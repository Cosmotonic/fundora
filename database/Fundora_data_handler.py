import mysql.connector
from database.Ctk_Fundora_data_config import db_config

def gem_person_data(email, data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    fields = ', '.join([f"{key} = %s" for key in data])
    values = list(data.values())
    values.append(email)

    query = f"UPDATE users SET {fields} WHERE email = %s"
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def hent_person_data(email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result
