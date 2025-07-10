USE fundora;
-- DROP TABLE IF EXISTS finansiering;

CREATE TABLE finansiering (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bruger_id INT NOT NULL,

    indtaegt_1 DECIMAL(12,2),
    pension_1 DECIMAL(5,2),
    opsparring_1 DECIMAL(12,2),
    gaeld_1 DECIMAL(12,2),

    indtaegt_2 DECIMAL(12,2),
    pension_2 DECIMAL(5,2),
    opsparring_2 DECIMAL(12,2),
    gaeld_2 DECIMAL(12,2),

    samlet_indtaegt DECIMAL(12,2),
    max_laan DECIMAL(12,2),
    lon_efter_skat1 DECIMAL(12,2),
    lon_efter_skat2 DECIMAL(12,2),
    skatteprocent1 DECIMAL(5,2),
    skatteprocent2 DECIMAL(5,2),
    samlet_efter_skat DECIMAL(12,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bruger_id) REFERENCES brugere(id)
);
