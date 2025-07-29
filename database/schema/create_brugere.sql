DESCRIBE brugere;
ALTER TABLE brugere
ADD COLUMN password VARCHAR(255);
ALTER TABLE brugere ADD COLUMN vil_kontaktes BOOLEAN DEFAULT 0;
ALTER TABLE brugere ADD COLUMN tillad_data BOOLEAN DEFAULT 0;

--- Indsæt brugerens betaling
ALTER TABLE brugere
ADD COLUMN user_role ENUM('free', 'premium') NOT NULL DEFAULT 'free',
ADD COLUMN payment_date DATETIME NULL;
ALTER TABLE brugere 
MODIFY COLUMN payment_date TIMESTAMP NULL DEFAULT NULL;
-- mysql.connector.errors.ProgrammingError: 1054 (42S22): Unknown column 'samletadresse1' in 'field list'

CREATE TABLE brugere (
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- Person 1
    fornavn1 VARCHAR(100),
    efternavn1 VARCHAR(100),
    telefon1 VARCHAR(20),
    mail1 VARCHAR(100) UNIQUE,
    adresse_vej1 VARCHAR(100),
    adresse_postnr1 VARCHAR(10),
    adresse_by1 VARCHAR(100),
    adresse_samlet1 VARCHAR(255),
    fodselsdag_dag1 INT,
    fodselsdag_maaned1 INT,
    fodselsdag_aar1 INT,
    dato_dmo1 VARCHAR(20),

    -- Person 2 (partner, ægtefælle, etc.)
    fornavn2 VARCHAR(100),
    efternavn2 VARCHAR(100),
    telefon2 VARCHAR(20),
    mail2 VARCHAR(100),
    adresse_vej2 VARCHAR(100),
    adresse_postnr2 VARCHAR(10),
    adresse_by2 VARCHAR(100),
    adresse_samlet2 VARCHAR(255),
    fodselsdag_dag2 INT,
    fodselsdag_maaned2 INT,
    fodselsdag_aar2 INT,
    dato_dmo2 VARCHAR(20),

    -- Supplerende oplysninger
    ny_adresse_vej VARCHAR(255),
    link_til_ny_adresse VARCHAR(255),
    rapportnavn VARCHAR(255),

    -- Login
    kodeord_hash VARCHAR(255),

    -- Meta
    oprettet_dato TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
