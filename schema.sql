DROP TABLE IF EXISTS inventory;

CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    itemName TEXT,
    description TEXT NOT NULL,
    location TEXT NOT NULL
);