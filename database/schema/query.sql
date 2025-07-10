USE fundora;
SHOW TABLES;
SHOW TABLES;
SHOW DATABASES;
INSERT INTO brugere (email, kode_hash) VALUES ('test@mail.com', '1234hash');
SELECT * FROM brugere;
SELECT * FROM finansiering;
SELECT * FROM udgift;
SELECT * FROM fremtid;

ALTER TABLE fremtid
DROP COLUMN realkredit_laaneberegning,
DROP COLUMN bank_laaneberegning;

SHOW COLUMNS FROM udgift;
SHOW COLUMNS FROM finansiering;
SHOW COLUMNS FROM brugere;
SHOW COLUMNS FROM fremtid;

SELECT * FROM brugere;
SELECT * FROM finansiering;
SELECT * FROM udgift;
SELECT * FROM fremtid;

SHOW COLUMNS FROM fundora_dictionaries;
SHOW COLUMNS FROM finansiering;

ALTER TABLE fremtid MODIFY COLUMN logged_in_email VARCHAR(255) FIRST;

ALTER TABLE fremtid MODIFY COLUMN bruger_id INT AUTO_INCREMENT PRIMARY KEY;


ALTER TABLE finansiering ADD COLUMN logged_in_email VARCHAR(255);
ALTER TABLE udgift ADD COLUMN logged_in_email VARCHAR(255);
ALTER TABLE fremtid ADD COLUMN logged_in_email VARCHAR(255);
ALTER TABLE brugere ADD COLUMN logged_in_email VARCHAR(255);


ALTER TABLE finansiering DROP COLUMN bruger_id;
ALTER TABLE finansiering DROP COLUMN id;

ALTER TABLE udgift DROP COLUMN bruger_id;
ALTER TABLE udgift DROP COLUMN id;

ALTER TABLE fremtid DROP COLUMN bruger_id;
ALTER TABLE fremtid DROP COLUMN id;

