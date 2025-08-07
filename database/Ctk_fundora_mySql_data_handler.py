import mysql.connector
from database.Ctk_Fundora_mySql_data_config import DB_CONFIG
import customtkinter as ctk
import json

# from database.Fundora_data_handler import gem_person_data

# GEM Data til databasen.  eksporter_data_til_db gem_person_data importer_data_fra_db hent_person_data
def eksporter_vars_til_db(email, data_dicts):

    for table_name, var_dict in data_dicts.items():
        print (f"TABEL NAME :::: {table_name}")
        gem_person_data(email, table_name, var_dict)


def gem_person_data(email, table_name, var_dict):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    data = {}
    for key, var in var_dict.items():
        try:
            value = var.get()
            # Hvis feltet er payment_date og værdien er tom streng → lav det til None (MySQL = NULL)
            if key.lower() == "payment_date" and (value == "" or value is None):
                value = None
            data[key.lower()] = value
        except Exception as e:
            print(f"Fejl ved hentning af '{key}': {e}")
    

    # Beskyt Premium-brugere, når de opgradere mens programmet et åbent. Undgå at overskrive user role på db
    if "user_role" in data and data["user_role"] == "free":
        cursor.execute(f"SELECT user_role FROM {table_name} WHERE logged_in_email = %s", (email,))
        current_role = cursor.fetchone()[0]
        if current_role == "premium":
            print(f"Springer user_role over for {email} (allerede premium).")
            del data["user_role"]
    # Check slutter her


    fields = ', '.join([f"{key} = %s" for key in data])
    values = list(data.values())
    values.append(email)

    # Tjek om rækken findes
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE logged_in_email = %s", (email,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        query = f"UPDATE {table_name} SET {fields} WHERE logged_in_email = %s"
        print(f"Opdaterer data i tabellen '{table_name}' for {email}")
    else:
        field_names = ', '.join(data.keys()) + ", logged_in_email"
        placeholders = ', '.join(["%s"] * (len(data) + 1))
        query = f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})"
        print(f"Indsætter ny række i tabellen '{table_name}' for {email}")

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


def eksporter_ugc_til_db(logged_in_email, ugc_dict):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Konverter til JSON-strenge
    json_data = {key: json.dumps(value) for key, value in ugc_dict.items()}
    print("JSON-klargjorte data til eksport:")
    for key, val in json_data.items():
        print(f"  {key}: {val}")

    # Byg SQL-delen
    columns = ', '.join(['logged_in_email'] + list(json_data.keys()))
    placeholders = ', '.join(['%s'] * (1 + len(json_data)))
    values = [logged_in_email] + list(json_data.values())

    update_clause = ', '.join([f"{key} = VALUES({key})" for key in json_data.keys()])

    query = f"""
        INSERT INTO ugc_data ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE
        {update_clause}
    """

    print("SQL forespørgsel klar:")
    print(query)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Data eksporteret til ugc_data.")
    except Exception as e:
        print("Fejl under eksport:", e)
    finally:
        cursor.close()
        connection.close()


# HENT data fra databasen. 
def importer_vars_fra_db(email, data_dicts):

    # iterate de forskellige dicts 
    for table_name, var_dict in data_dicts.items():
        data = hent_person_data(email, table_name)

        if not data:
            print(f"Ingen data fundet i tabellen '{table_name}' for bruger.")
            continue
        
        # 
        for key, var in var_dict.items():
            try:
                value = data.get(key.lower())
                if value is not None:
                    var.set(value)
                else:
                    var.set("" if isinstance(var, ctk.StringVar) else 0)
            except Exception as e:
                print(f"Fejl ved indsætning af '{key}' i '{table_name}': {e}")


def hent_person_data(email, table_name):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM {table_name} WHERE logged_in_email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    return result


def importer_ugc_fra_db(logged_in_email, target_dicts):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ugc_data WHERE logged_in_email = %s", (logged_in_email,))
        row = cursor.fetchone()

        if not row:
            print("Ingen data fundet for bruger:", logged_in_email)
            return

        columns = [desc[0] for desc in cursor.description]
        data_dict = dict(zip(columns, row))

        for key, target_dict in target_dicts.items():
            if key not in data_dict:
                continue
            try:
                json_data = json.loads(data_dict[key])
                target_dict.clear() # clear local dict. 
                target_dict.update(json_data) # update local dict with db dict. 
                #print(f"Importerede {key}: {json_data}") # Fx: "feedback": self.feedback_dict,
            except Exception as e:
                print(f"Kunne ikke loade JSON for {key}: {e}")

    except Exception as e:
        print("Fejl under import:", e)
    finally:
        cursor.close()
        connection.close()


# After payment - updates in the flask (webhook)
def update_user_to_premium(email):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM brugere WHERE logged_in_email = %s", (email,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            query = """
                UPDATE brugere
                SET user_role = %s, payment_date = NOW()
                WHERE logged_in_email = %s
            """
            values = ('premium', email)
            cursor.execute(query, values)
            connection.commit()
            print(f"Bruger '{email}' opdateret til premium.")
            return True
        else:
            print(f"Bruger '{email}' blev ikke fundet i databasen. Ingen opdatering udført.")
            return False

    except Exception as e:
        print(f"Fejl under opdatering af premium-status for '{email}': {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
