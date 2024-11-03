CREATE TABLE IF NOT EXISTS result (
    uuid TEXT PRIMARY KEY,
    name_1 TEXT,
    name_2 TEXT,
    name_1_desc TEXT,
    name_2_desc TEXT,
    name_1_occupation TEXT,
    name_2_occupation TEXT,
    loading_screen_1 TEXT,
    loading_screen_2 TEXT,
    match_score INTEGER,
    car_score INTEGER,
    meeting_score INTEGER,
    ikea_score INTEGER,
    fight_score INTEGER,
    losing_score INTEGER,
    marriage_score INTEGER
);

INSERT INTO result VALUES ("118230ca-e0e8-43c5-9f5e-4a787f3d9405", "Becky", "Ben", NULL, NULL, NULL, NULL, NULL, NULL, 57, 10, 20, 30, 50, 70, 63);
INSERT INTO result VALUES ("62ad919d-df86-468e-8fcc-0b1b33a48d6f", "Hubert", "Alastair", NULL, NULL, NULL, NULL, NULL, NULL, 93, 10, 20, 30, 50, 70, 63);
INSERT INTO result VALUES ("becbad47-90a6-442e-9e76-5edcc2c0568a", "John", "Joan", NULL, NULL, NULL, NULL, NULL, NULL, 17, 10, 20, 30, 50, 70, 63);