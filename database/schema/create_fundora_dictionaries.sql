

CREATE TABLE fundora_dictionaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bruger_email VARCHAR(100) NOT NULL,
    data_navn VARCHAR(100) NOT NULL,         -- fx 'realkredit_laaneberegning'
    data_json LONGTEXT NOT NULL,             -- JSON-serialiseret indhold
    oprettet_dato TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_user_data (bruger_email, data_navn)
);