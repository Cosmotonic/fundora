DROP TABLE IF EXISTS udgift;

CREATE TABLE udgift (
    logged_in_email VARCHAR(255),

    bolig_udgift DECIMAL(12,2),
    forbrug DECIMAL(12,2),
    mad_dagligvare DECIMAL(12,2),
    transport DECIMAL(12,2),
    forsikringer DECIMAL(12,2),
    telefon_int_medie DECIMAL(12,2),
    personlig_pleje_toej DECIMAL(12,2),
    fritid_fornoejelser DECIMAL(12,2),
    pasning_fritidsaktiv DECIMAL(12,2),

    flex_udgift_string1 VARCHAR(255),
    flex_udgift_var1 DECIMAL(12,2),
    flex_udgift_string2 VARCHAR(255),
    flex_udgift_var2 DECIMAL(12,2),
    flex_udgift_string3 VARCHAR(255),
    flex_udgift_var3 DECIMAL(12,2),

    gaeldsfaktor DECIMAL(5,2),
    banklaan DECIMAL(12,2),
    realkreditlaan DECIMAL(12,2),
    samlet_laan DECIMAL(12,2),
    alle_faste_udgifter DECIMAL(12,2),
    forventet_pris DECIMAL(12,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
