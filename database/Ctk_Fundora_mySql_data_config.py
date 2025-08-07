
# 

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Acmv13d2tv2450kbhsv*',
    'database': 'fundora'
}



# for online connection 
'''

import mysql.connector

DB_CONFIG = {
    'host': 'ctk-fundora-db.mysql.database.azure.com',
    'user': 'larssongu',
    'password': 'Test1234!',
    'database': 'mysql',
    'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Forbindelse virker!")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Fejl: {err.errno} - {err.msg}")

'''
