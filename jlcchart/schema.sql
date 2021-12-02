DROP TABLE IF EXISTS components;
DROP TABLE IF EXISTS fetchlist;

CREATE TABLE IF NOT EXISTS components (
    id INTEGER,
    [timestamp] timestamp,
    data TEXT
);

CREATE TABLE IF NOT EXISTS fetchlist (
    id INTEGER,
    code TEXT
);
