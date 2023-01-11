CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE fighters (
  id SERIAL PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  nickname TEXT,
  born DATE,
  height REAL,
  weight SMALLINT,
  country SMALLINT REFERENCES countries(id)
);

CREATE TABLE referees (
  id SERIAL PRIMARY KEY,
  firstname TEXT,
  lastname TEXT
);

CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  abbreviation CHAR(3) NOT NULL
);

CREATE TABLE fights (
  id SERIAL PRIMARY KEY,
  fighter1 INTEGER REFERENCES fighters(id) NOT NULL,
  fighter2 INTEGER REFERENCES fighters(id) NOT NULL,
  referee INTEGER REFERENCES referees(id) DEFAULT 1,
  rounds SMALLINT DEFAULT 3 NOT NULL,
  ending_time TIME,  
  winner INTEGER REFERENCES fighters(id) NOT NULL,
  draw BOOLEAN DEFAULT FALSE,
  winning_method TEXT,
  date TIMESTAMP NOT NULL,
  event INTEGER,
  fight_order INTEGER,
  weight_class SMALLINT NOT NULL,
  CONSTRAINT unique_fight UNIQUE (fighter1, fighter2, date)
);


CREATE INDEX event_idx ON fights (event);

CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  date DATE NOT NULL,
  location TEXT NOT NULL,
  promotion TEXT NOT NULL,
  CONSTRAINT unique_event UNIQUE (name, date)
);

CREATE INDEX promotion_idx ON events (promotion);