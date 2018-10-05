DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS record;

CREATE TABLE station (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stationname TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  station_id INTEGER NOT NULL,
  timepoint TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  temperature REAL, -- Can be null, since not every sensor delivers this value
  humidity REAL, -- Can be null, since not every sensor delivers this value
  pressure REAL, -- Can be null, since not every sensor delivers this value
  FOREIGN KEY (station_id) REFERENCES station (id)
);
