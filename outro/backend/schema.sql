CREATE TABLE Water_Data (
    id SERIAL PRIMARY KEY,

    ph REAL,
    hardness REAL,
    solids REAL,
    chloramines REAL,
    sulfate REAL,
    conductivity REAL,
    organic_carbon REAL,
    trihalomethanes REAL,
    turbidity REAL,
    probability REAL,
    potability INTEGER,
    prediction TEXT NOT NULL,
    
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

SELECT * FROM Water_Data;