import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="fundora_user",
    password="Acmv13d2tv2450kbhsv*",
    database="fundora"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")

for table in cursor:
    print(table)

cursor.close()
conn.close()


