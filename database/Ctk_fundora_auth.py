import mysql.connector
import bcrypt
from database.Ctk_Fundora_data_config import DB_CONFIG

# Konfiguration til din database
# Dette bruges til at oprette forbindelse til din MySQL database
# Du kan genbruge dette dictionary i hele din applikation, når du skal forbinde


# Helper-funktion som returnerer en aktiv forbindelse til databasen
def get_mysql_connection():
    return mysql.connector.connect(**DB_CONFIG)


# Funktion til at oprette en ny bruger i tabellen "bruger"
def register_user(email, password):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Vi antager at tabellen "bruger" har kolonnerne: mail1 og password
        cursor.execute("INSERT INTO brugere (logged_in_email, password) VALUES (%s, %s)", (email, hashed_pw))
        conn.commit()
        print("brugere oprettet.")

    except mysql.connector.IntegrityError:
        print("Email findes allerede.")

    finally:
        cursor.close()
        conn.close()


# Funktion til at logge en bruger ind
def login_user(email, password):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()

        # Hent den gemte hashed adgangskode fra databasen
        cursor.execute("SELECT password FROM brugere WHERE logged_in_email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            print("brugere ikke fundet.")
            return False

        # Sammenlign brugerens indtastede kode med den hashed kode i databasen
        elif bcrypt.checkpw(password.encode(), result[0].encode()):
            print("Login succesfuldt!")
            return True

        else:
            print("Forkert adgangskode.")
            return False

    finally:
        cursor.close()
        conn.close()

