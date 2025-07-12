DROP TABLE IF EXISTS budgetvaerktoej;

CREATE TABLE budgetvaerktoej (
    logged_in_email VARCHAR(255),

    budget_titel VARCHAR(255),
    kontakt_navn VARCHAR(255),
    kontakt_telefon VARCHAR(50),
    kontakt_mail VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
