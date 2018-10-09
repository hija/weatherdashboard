DROP TABLE IF EXISTS sensor;
DROP TABLE IF EXISTS record;

CREATE TABLE sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensorname TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id INTEGER NOT NULL,
  timepoint TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  temperature REAL, -- Can be null, since not every sensor delivers this value
  humidity REAL, -- Can be null, since not every sensor delivers this value
  pressure REAL, -- Can be null, since not every sensor delivers this value
  FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);
