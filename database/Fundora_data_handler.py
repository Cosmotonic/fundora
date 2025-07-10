import mysql.connector
from database.Ctk_Fundora_data_config import DB_CONFIG

def gem_person_data(email, data):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    fields = ', '.join([f"{key} = %s" for key in data])
    values = list(data.values())
    values.append(email)

    query = f"UPDATE brugere SET {fields} WHERE mail1 = %s"

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def hent_person_data(email):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM brugere WHERE mail1 = %s"

    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result




def gem_personlige_oplysninger(bruger_id, oplysninger_dict):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE brugere SET
            fornavn1 = %s,
            efternavn1 = %s,
            telefon1 = %s,
            adresse_vej1 = %s,
            adresse_postnr1 = %s,
            adresse_by1 = %s,
            adresse_samlet1 = %s,
            fodselsdag_dag1 = %s,
            fodselsdag_maaned1 = %s,
            fodselsdag_aar1 = %s
        WHERE id = %s
    """

    data = (
        oplysninger_dict["fornavn1"],
        oplysninger_dict["efternavn1"],
        oplysninger_dict["telefon1"],
        oplysninger_dict["adresse_vej1"],
        oplysninger_dict["adresse_postnr1"],
        oplysninger_dict["adresse_by1"],
        oplysninger_dict["adresse_samlet1"],
        oplysninger_dict["fodselsdag_dag1"],
        oplysninger_dict["fodselsdag_maaned1"],
        oplysninger_dict["fodselsdag_aar1"],
        bruger_id
    )

    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Personlige oplysninger opdateret.")
    except Exception as e:
        print("Fejl ved opdatering:", e)
    finally:
        conn.close()
