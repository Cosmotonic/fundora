DROP TABLE IF EXISTS fremtid;

CREATE TABLE fremtid (
    logged_in_email VARCHAR(255),

    bolig_udgift DECIMAL(12,2),
    realkredit_laaneperiode INT,
    realkredit_nominel DECIMAL(5,2),
    realkredit_bidragssats DECIMAL(5,2),
    realkredit_terminer INT,
    afdragsfri BOOLEAN,

    bank_nominel DECIMAL(5,2),
    bank_terminer INT,
    bank_laaneperiode INT,

    rente_betaling DECIMAL(10,2),
    rente_afdrag DECIMAL(10,2),
    rentefradrag DECIMAL(10,2),
    rentefradrag_procent DECIMAL(5,2),
    samlet_ydelse DECIMAL(10,2),
    fast_udgifter DECIMAL(10,2),
    fast_udgifter_inkl_ydelser DECIMAL(10,2),
    raadighedsbeloeb DECIMAL(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
