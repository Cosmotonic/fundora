DROP TABLE IF EXISTS forhandling;

CREATE TABLE forhandling (
    logged_in_email VARCHAR(255),

    udbudspris DECIMAL(12,2),
    forventet_procent DECIMAL(5,2),
    forventet_pris DECIMAL(12,2),

    runde1_procent DECIMAL(5,2),
    runde1_pris DECIMAL(12,2),
    runde2_procent DECIMAL(5,2),
    runde2_pris DECIMAL(12,2),
    runde3_procent DECIMAL(5,2),
    runde3_pris DECIMAL(12,2),
    runde4_procent DECIMAL(5,2),
    runde4_pris DECIMAL(12,2),

    aggressivitet INT,

    forhandling_titel VARCHAR(255),
    strategi_titel VARCHAR(255),
    losore_titel VARCHAR(255),
    argument_titel VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
