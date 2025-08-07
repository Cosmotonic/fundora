import sqlite3
from database.schema.Ctk_fundora_sqllite_schemas import *
# from database.sqlite_tables import create_table_brugere  # eller samme fil

def initialize_sqlite_db():
    conn = sqlite3.connect("fundora_data.db")
    cursor = conn.cursor()

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
