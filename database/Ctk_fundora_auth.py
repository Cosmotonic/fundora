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
        cursor.execute("INSERT INTO brugere (mail1, password) VALUES (%s, %s)", (email, hashed_pw))
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
        cursor.execute("SELECT password FROM brugere WHERE mail1 = %s", (email,))
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


# Funktion til at opdatere brugerens data (f.eks. loen1, alder osv.)
# "data" er en dictionary med felter: {"loen1": 50000, "alder": 36}
def save_user_data(email, data):
    if not data:
        print("Ingen data at gemme.")
        return

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Dynamisk SQL: loen1 = %s, alder = %s, osv.
    fields = ', '.join([f"{key} = %s" for key in data])
    values = list(data.values()) + [email]

    sql = f"UPDATE brugere SET {fields} WHERE mail1 = %s"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    print(f"Data gemt for {email}: {data}")


# Funktion til at hente ALLE data om brugeren som dictionary
def get_user_data(email):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM brugere WHERE mail1 = %s", (email,))
    row = cursor.fetchone()
    col_names = [desc[0] for desc in cursor.description]

    conn.close()

    if row:
        return dict(zip(col_names, row))
    else:
        return None
    

if __name__ == "__main__":
    register_user("kasper@voca.com", "mitKodeord123")



save_user_data("kasper@voca.com", {
    "fornavn1": "Kasper",
    "efternavn1": "Larsson",
    "adresse_vej1": "Testvej 12"
})