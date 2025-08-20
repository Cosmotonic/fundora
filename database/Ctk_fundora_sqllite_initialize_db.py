import sqlite3
from database.schema.Ctk_fundora_sqllite_schemas import *
import os


# Creates a local database on the users computer. 
# Used when the program is opened by a user for the first time

def get_db_path():
    appdata = os.getenv("APPDATA")  # fx C:\Users\Kasper\AppData\Roaming
    fundora_dir = os.path.join(appdata, "Fundora")
    os.makedirs(fundora_dir, exist_ok=True)
    return os.path.join(fundora_dir, "fundora_data.db")


def initialize_sqlite_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #conn = sqlite3.connect("fundora_data.db")
    #cursor = conn.cursor()

    create_table_brugere(cursor)
    create_table_fremtid(cursor)
    create_table_finansiering(cursor)
    create_table_udgift(cursor)
    create_table_budgetvaerktoej(cursor)
    create_table_forhandling(cursor)
    create_table_ugc_data(cursor)

    conn.commit()
    conn.close()
    print("✅ SQLite-database initialiseret.")
