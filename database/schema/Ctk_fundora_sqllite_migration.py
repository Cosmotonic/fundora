import decimal
import sqlite3
import mysql.connector
from datetime import datetime

# --- LOKAL MySQL KONFIG ---
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Acmv13d2tv2450kbhsv*',
    'database': 'fundora'
}

# --- Funktion til at rydde værdier før indsættelse i SQLite ---
def clean_value_for_sqlite(value):
    if isinstance(value, decimal.Decimal):
        return float(value)
    elif isinstance(value, datetime):
        return value.isoformat(sep=" ")
    else:
        return value

# --- Forbindelser ---
mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
mysql_cursor = mysql_conn.cursor(dictionary=True)

sqlite_conn = sqlite3.connect("fundora_data.db")
sqlite_cursor = sqlite_conn.cursor()

# --- Tabelnavne ---
tables = [
    "brugere",
    "fremtid",
    "finansiering",
    "udgift",
    "budgetvaerktoej",
    "forhandling",
    "ugc_data"
]

for table in tables:
    print(f"⏳ Migrerer: {table}")
    mysql_cursor.execute(f"SELECT * FROM {table}")
    rows = mysql_cursor.fetchall()

    if not rows:
        print(f"⚠️  Ingen data fundet i {table}, springer over.")
        continue

    column_names = rows[0].keys()
    placeholders = ", ".join(["?"] * len(column_names))
    insert_query = f"""
        INSERT INTO {table} ({", ".join(column_names)})
        VALUES ({placeholders})
    """

    for row in rows:
        cleaned_row = [clean_value_for_sqlite(v) for v in row.values()]
        try:
            sqlite_cursor.execute(insert_query, cleaned_row)
        except sqlite3.IntegrityError as e:
            print(f"❌ Fejl i {table}: {e}")
        except Exception as e:
            print(f"‼️ Ukendt fejl i {table}: {e}")

sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()
print("✅ Migration fuldført med lokal database.")






'''
import decimal

import sqlite3
import mysql.connector
from datetime import datetime

# --- LOKAL MySQL KONFIG ---
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Acmv13d2tv2450kbhsv*',
    'database': 'fundora'
}

# --- Forbindelser ---
mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
mysql_cursor = mysql_conn.cursor(dictionary=True)

sqlite_conn = sqlite3.connect("fundora_data.db")
sqlite_cursor = sqlite_conn.cursor()

# --- Tabelnavne (ingen ændringer i kolonner) ---
tables = [
    "brugere",
    "fremtid",
    "finansiering",
    "udgift",
    "budgetvaerktoej",
    "forhandling",
    "ugc_data"
]

for table in tables:
    print(f"⏳ Migrerer: {table}")
    mysql_cursor.execute(f"SELECT * FROM {table}")
    rows = mysql_cursor.fetchall()

    if not rows:
        print(f"⚠️  Ingen data fundet i {table}, springer over.")
        continue

    column_names = rows[0].keys()
    placeholders = ", ".join(["?"] * len(column_names))
    insert_query = f"""
        INSERT INTO {table} ({", ".join(column_names)})
        VALUES ({placeholders})
    """

    for row in rows:
        cleaned_row = []

        for value in row.values():
            if isinstance(value, datetime):
                cleaned_row.append(value.isoformat(sep=" "))
            elif isinstance(value, decimal.Decimal):
                cleaned_row.append(float(value))
            else:
                cleaned_row.append(value)
        try:
            sqlite_cursor.execute(insert_query, cleaned_row)
        except sqlite3.IntegrityError as e:
            print(f"❌ Fejl i {table}: {e}")
        except Exception as e:
            print(f"‼️ Ukendt fejl i {table}: {e}")

sqlite_conn.commit()
sqlite_conn.close()
mysql_conn.close()
print("✅ Migration fuldført med lokal database.")
'''