-- Create database
CREATE DATABASE dorixona_x;

-- Connect to database
\c dorixona_x;

-- Create medicines table
CREATE TABLE dorilar_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    price NUMERIC(10,2),
    quantity INTEGER,
    expiry_date DATE
);

-- Insert 100 sample medicines
INSERT INTO dorilar_table (name, manufacturer, price, quantity, expiry_date)
SELECT
    'Medicine_' || i,
    'PharmaCompany_' || (i % 10 + 1),
    ROUND((random()*50 + 5)::numeric,2),
    (random()*200)::int,
    CURRENT_DATE + (random()*900)::int
FROM generate_series(1,100) AS s(i);

-- View inserted data
SELECT * FROM dorilar_table;