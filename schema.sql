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
  fighter1 INTEGER REFERENCES fighters(id) NOT NULL ON DELETE CASCADE,
  fighter2 INTEGER REFERENCES fighters(id) NOT NULL ON DELETE CASCADE,
  referee INTEGER REFERENCES referees(id) DEFAULT 1 NOT NULL ON DELETE CASCADE,
  rounds SMALLINT DEFAULT 3 NOT NULL,
  ending_time TIME,  
  winner INTEGER REFERENCES fighters(id) ON DELETE CASCADE,
  draw BOOLEAN DEFAULT FALSE,
  winning_method TEXT,
  date DATE NOT NULL,
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

CREATE TABLE scorecards (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  fight INTEGER REFERENCES fights(id) ON DELETE CASCADE,
  score_f1 SMALLINT,
  score_f2 SMALLINT,
  comment TEXT
  CONSTRAINT unique_scorecard UNIQUE (username, fight)
);