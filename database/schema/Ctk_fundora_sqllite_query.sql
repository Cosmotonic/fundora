--- right click og vælg run query (eller ctrl + shift + Q)
---OBS: husk der er foreskel på "run query" og "run selected query" 



DELETE FROM brugere WHERE mail1 = 'test2@example.com';


SELECT * FROM brugere;
SELECT * FROM udgift;
SELECT * FROM finansiering;
SELECT * FROM fremtid;
SELECT * FROM ugc_data;

INSERT INTO brugere (logged_in_email, fornavn1, efternavn1, telefon1, mail1)
VALUES ('test2@example.com', 'Kasper', 'Larsson', '12345678', 'test2@example.com');
