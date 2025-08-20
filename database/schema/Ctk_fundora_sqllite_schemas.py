def create_table_brugere(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brugere (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logged_in_email TEXT,
            fornavn1 TEXT,
            efternavn1 TEXT,
            telefon1 TEXT,
            mail1 TEXT UNIQUE,
            adresse_vej1 TEXT,
            adresse_postnr1 TEXT,
            adresse_by1 TEXT,
            adresse_samlet1 TEXT,
            fodselsdag_dag1 INTEGER,
            fodselsdag_maaned1 INTEGER,
            fodselsdag_aar1 INTEGER,
            dato_dmo1 TEXT,
            fornavn2 TEXT,
            efternavn2 TEXT,
            telefon2 TEXT,
            mail2 TEXT,
            adresse_vej2 TEXT,
            adresse_postnr2 TEXT,
            adresse_by2 TEXT,
            adresse_samlet2 TEXT,
            fodselsdag_dag2 INTEGER,
            fodselsdag_maaned2 INTEGER,
            fodselsdag_aar2 INTEGER,
            dato_dmo2 TEXT,
            ny_adresse_vej TEXT,
            link_til_ny_adresse TEXT,
            rapportnavn TEXT,
            kodeord_hash TEXT,
            oprettet_dato TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            password TEXT,
            vil_kontaktes INTEGER DEFAULT 0,
            tillad_data INTEGER DEFAULT 0,
            user_role TEXT DEFAULT 'free',
            payment_date TIMESTAMP
        );
    """)



def create_table_fremtid(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fremtid (
            logged_in_email TEXT PRIMARY KEY,
            bolig_udgift REAL,
            realkredit_laaneperiode INTEGER,
            realkredit_nominel REAL,
            realkredit_bidragssats REAL,
            realkredit_terminer INTEGER,
            afdragsfri INTEGER,
            bank_nominel REAL,
            bank_terminer INTEGER,
            bank_laaneperiode INTEGER,
            rente_betaling REAL,
            rente_afdrag REAL,
            rentefradrag REAL,
            rentefradrag_procent REAL,
            samlet_ydelse REAL,
            fast_udgifter REAL,
            fast_udgifter_inkl_ydelser REAL,
            raadighedsbeloeb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_finansiering(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finansiering (
            logged_in_email TEXT PRIMARY KEY,
            indtaegt_1 REAL,
            pension_1 REAL,
            opsparring_1 REAL,
            gaeld_1 REAL,
            indtaegt_2 REAL,
            pension_2 REAL,
            opsparring_2 REAL,
            gaeld_2 REAL,
            samlet_indtaegt REAL,
            max_laan REAL,
            lon_efter_skat1 REAL,
            lon_efter_skat2 REAL,
            skatteprocent1 REAL,
            skatteprocent2 REAL,
            samlet_efter_skat REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_udgift(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS udgift (
            logged_in_email TEXT PRIMARY KEY,
            bolig_udgift REAL,
            forbrug REAL,
            mad_dagligvare REAL,
            transport REAL,
            forsikringer REAL,
            telefon_int_medie REAL,
            personlig_pleje_toej REAL,
            fritid_fornoejelser REAL,
            pasning_fritidsaktiv REAL,
            flex_udgift_string1 TEXT,
            flex_udgift_var1 REAL,
            flex_udgift_string2 TEXT,
            flex_udgift_var2 REAL,
            flex_udgift_string3 TEXT,
            flex_udgift_var3 REAL,
            gaeldsfaktor REAL,
            banklaan REAL,
            realkreditlaan REAL,
            samlet_laan REAL,
            alle_faste_udgifter REAL,
            forventet_pris REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_budgetvaerktoej(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgetvaerktoej (
            logged_in_email TEXT PRIMARY KEY,
            budget_titel TEXT,
            kontakt_navn TEXT,
            kontakt_telefon TEXT,
            kontakt_mail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_budgetvaerktoej(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgetvaerktoej (
            logged_in_email TEXT PRIMARY KEY,
            budget_titel TEXT,
            kontakt_navn TEXT,
            kontakt_telefon TEXT,
            kontakt_mail TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_forhandling(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forhandling (
            logged_in_email TEXT PRIMARY KEY,
            udbudspris REAL,
            forventet_procent REAL,
            forventet_pris REAL,
            runde1_procent REAL,
            runde1_pris REAL,
            runde2_procent REAL,
            runde2_pris REAL,
            runde3_procent REAL,
            runde3_pris REAL,
            runde4_procent REAL,
            runde4_pris REAL,
            aggressivitet INTEGER,
            forhandling_titel TEXT,
            strategi_titel TEXT,
            losore_titel TEXT,
            argument_titel TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
def create_table_ugc_data(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ugc_data (
            logged_in_email TEXT PRIMARY KEY,
            argumentation TEXT,
            loesoere TEXT,
            budgetvaerktoej TEXT,
            feedback TEXT, 
            user_notes TEXT
        );
    """)

