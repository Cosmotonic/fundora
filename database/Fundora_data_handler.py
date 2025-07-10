import mysql.connector
from database.Ctk_Fundora_data_config import DB_CONFIG
import customtkinter as ctk

# from database.Fundora_data_handler import gem_person_data

# GEM Data til databasen.  eksporter_data_til_db gem_person_data importer_data_fra_db hent_person_data
def eksporter_data_til_db(email, data_dicts):

    for table_name, var_dict in data_dicts.items():
        print (f"TABEL NAME :::: {table_name}")
        print (f"TABEL NAME :::: {table_name}")
        gem_person_data(email, table_name, var_dict)


def gem_person_data(email, table_name, var_dict):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    data = {}
    for key, var in var_dict.items():
        try:
            data[key.lower()] = var.get()
        except Exception as e:
            print(f"Fejl ved hentning af '{key}': {e}")
 
    # (1. data = {"indtaegt_1": 50000, "pension_1": 10} # (2. ["indtaegt_1 = %s", "pension_1 = %s"] # (3 "indtaegt_1 = %s, pension_1 = %s" 
    fields = ', '.join([f"{key} = %s" for key in data]) # bliver brugt i UPDATE
    values = list(data.values())
    values.append(email) # (1. values = [50000, 10, "kasper@voca.com"] # (2 Husk MySql skiller værdier til en liste og struktur til en liste. 

    # Tjek om rækken findes
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE logged_in_email = %s", (email,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        # UPDATE
        query = f"UPDATE {table_name} SET {fields} WHERE logged_in_email = %s" # Opdaterer data i tabellen 'fremtid' for kasper@voca.com
        print(f"Opdaterer data i tabellen '{table_name}' for {email}")
    else:
        # INSERT
        field_names = ', '.join(data.keys()) + ", logged_in_email"
        placeholders = ', '.join(["%s"] * (len(data) + 1))
        query = f"INSERT INTO {table_name} ({field_names}) VALUES ({placeholders})"
        print(f"Indsætter ny række i tabellen '{table_name}' for {email}")

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()



# HENT data fra databasen. 
def importer_data_fra_db(email, data_dicts):

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

