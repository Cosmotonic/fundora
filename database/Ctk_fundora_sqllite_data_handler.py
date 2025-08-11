import mysql.connector
from database.Ctk_Fundora_mySql_data_config import DB_CONFIG
import customtkinter as ctk
import json
import sqlite3

DB_NAME = "fundora_data.db"

# from database.Fundora_data_handler import gem_person_data


def eksporter_vars_til_db(email, data_dicts):
    for table_name, var_dict in data_dicts.items():
        # print(f"TABEL NAME :::: {table_name}")
        gem_person_data(email, table_name, var_dict)

def gem_person_data(email, table_name, var_dict):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    data = {}
    for key, var in var_dict.items():
        try:
            value = var.get()
            if key.lower() == "payment_date" and (value == "" or value is None):
                value = None
            data[key.lower()] = value
        except Exception as e:
            pass 
            # print(f"Fejl ved hentning af '{key}': {e}")

    # Beskyt Premium-brugere, undgå overskrivning af user_role
    if "user_role" in data and data["user_role"] == "free":
        cursor.execute(f"SELECT user_role FROM {table_name} WHERE logged_in_email = ?", (email,))
        result = cursor.fetchone()
        if result and result[0] == "premium":
            # print(f"Springer user_role over for {email} (allerede premium).")
            del data["user_role"]

    fields = ', '.join([f"{key} = ?" for key in data])
    values = list(data.values())
    values.append(email)

    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE logged_in_email = ?", (email,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        query = f"UPDATE {table_name} SET {fields} WHERE logged_in_email = ?"
        #print(f"Opdaterer data i tabellen '{table_name}' for {email}")
    else:
        field_names = ', '.join(data.keys()) + ", logged_in_email"
        placeholders = ', '.join(["?"] * (len(data) + 1))
        query = f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})"
        #print(f"Indsætter ny række i tabellen '{table_name}' for {email}")

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()



def eksporter_ugc_til_db(logged_in_email, ugc_dict):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Konverter til JSON-strenge
    json_data = {key: json.dumps(value) for key, value in ugc_dict.items()}
    # print("JSON-klargjorte data til eksport:")
    for key, val in json_data.items():
        pass
        #print(f"  {key}: {val}")

    columns = ', '.join(['logged_in_email'] + list(json_data.keys()))
    placeholders = ', '.join(['?'] * (1 + len(json_data)))
    values = [logged_in_email] + list(json_data.values())

    query = f"""
        INSERT OR REPLACE INTO ugc_data ({columns})
        VALUES ({placeholders})
    """

    #print("SQLite SQL forespørgsel klar:")
    #print(query)

    try:
        cursor.execute(query, values)
        connection.commit()
        #print("Data eksporteret til ugc_data.")
    except Exception as e:
        pass
        #print("Fejl under eksport:", e)
    finally:
        cursor.close()
        connection.close()



def importer_vars_fra_db(email, data_dicts):
    for table_name, var_dict in data_dicts.items():
        data = hent_person_data(email, table_name)

        if not data:
            #print(f"Ingen data fundet i tabellen '{table_name}' for bruger.")
            continue
        
        for key, var in var_dict.items():
            try:
                value = data.get(key.lower())
                if value is not None:
                    var.set(value)
                else:
                    var.set("" if isinstance(var, ctk.StringVar) else 0)
            except Exception as e:
                pass
                #print(f"Fejl ved indsætning af '{key}' i '{table_name}': {e}")

def hent_person_data(email, table_name):
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row  # gør det muligt at få dictionary-lignende rows
    cursor = connection.cursor()

    query = f"SELECT * FROM {table_name} WHERE logged_in_email = ?"
    cursor.execute(query, (email,))
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None
    else:
        return dict(row)



def importer_ugc_fra_db(logged_in_email, target_dicts):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ugc_data WHERE logged_in_email = ?", (logged_in_email,))
        row = cursor.fetchone()

        if not row:
            #print("Ingen data fundet for bruger:", logged_in_email)
            return

        # Kolonnenavne
        columns = [description[0] for description in cursor.description]
        data_dict = dict(zip(columns, row))

        for key, target_dict in target_dicts.items():
            if key not in data_dict or data_dict[key] is None:
                continue
            try:
                json_data = json.loads(data_dict[key])
                target_dict.clear()  # tøm lokal dict
                target_dict.update(json_data)  # opdater med db data
            except Exception as e:
                pass 
                # print(f"Kunne ikke loade JSON for {key}: {e}")

    except Exception as e:
        pass
        #print("Fejl under import:", e)
    finally:
        cursor.close()
        connection.close()


def update_user_to_premium(email):
    connection = None
    cursor = None
    try:
        connection = sqlite3.connect(DB_NAME)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM brugere WHERE logged_in_email = ?", (email,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            query = """
                UPDATE brugere
                SET user_role = ?, payment_date = CURRENT_TIMESTAMP
                WHERE logged_in_email = ?
            """
            cursor.execute(query, ('premium', email))
            connection.commit()
            #print(f"Bruger '{email}' opdateret til premium.")
            return True
        else:
            #print(f"Bruger '{email}' blev ikke fundet i databasen. Ingen opdatering udført.")
            return False

    except Exception as e:
        #print(f"Fejl under opdatering af premium-status for '{email}': {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
