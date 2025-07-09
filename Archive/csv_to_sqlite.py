import csv
import sqlite3

# Connect or create the DB file
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        name TEXT,
        address TEXT
    )
''')

# Read from CSV and insert rows
with open("users.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT OR REPLACE INTO users (email, password, name, address)
            VALUES (?, ?, ?, ?)
        ''', (row['email'], row['password'], row['name'], row['address']))

# Save and close
conn.commit()
conn.close()
