import mysql.connector
import bcrypt
from database.Ctk_Fundora_mySql_data_config import DB_CONFIG

# Konfiguration til din database
# Dette bruges til at oprette forbindelse til din MySQL database
# Du kan genbruge dette dictionary i hele din applikation, når du skal forbinde

# Helper-funktion som returnerer en aktiv forbindelse til databasen
'''
def get_mysql_connection():
    return mysql.connector.connect(**DB_CONFIG)
'''
import sqlite3
from database.Ctk_fundora_sqllite_initialize_db import get_db_path

def get_sqlite_connection():
    return sqlite3.connect(get_db_path())

# Funktion til at logge en bruger ind
def login_user(email, password):
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM brugere WHERE logged_in_email = ?", (email,))
        result = cursor.fetchone()

        if result is None:
            print("Bruger ikke fundet.")
            return False

        # Sammenlign hash
        elif bcrypt.checkpw(password.encode(), result[0].encode()):
            print("Login succesfuldt!")
            return True
        else:
            print("Forkert adgangskode.")
            return False

    finally:
        cursor.close()
        conn.close()


def register_user(email, password, fornavn, efternavn, telefon, tillad_data, vil_kontaktes):
    if not tillad_data:
        print("Brugeren accepterede ikke databehandling.")
        return "no_data_consent"

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()

        # Tjek om mail allerede findes
        cursor.execute("SELECT * FROM brugere WHERE logged_in_email = ?", (email,))
        if cursor.fetchone():
            return "email_exists"

        # Indsæt bruger
        cursor.execute("""
            INSERT INTO brugere (
                logged_in_email, mail1, password,
                fornavn1, efternavn1, telefon1,
                tillad_data, vil_kontaktes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email,
            email,
            hashed_pw.decode("utf-8"),  # gem som tekst
            fornavn,
            efternavn,
            telefon,
            int(tillad_data),
            int(vil_kontaktes)
        ))

        conn.commit()
        print("Bruger oprettet.")
        return "success"

    except sqlite3.Error as e:
        print("Databasefejl:", e)
        return "db_error"

    finally:
        cursor.close()
        conn.close()
