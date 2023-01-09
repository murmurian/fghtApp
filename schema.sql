CREATE TABLE fighters (
  id INTEGER PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  nickname TEXT,
  born DATE,
  height REAL,
  weight SMALLINT,
  country SMALLINT REFERENCES countries(id)
);

CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  abbreviation CHAR(3) NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  admin BOOLEAN DEFAULT FALSE
);