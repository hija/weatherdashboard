
def sensor_exists(db, sensorname):
    return get_sensor_id(db, sensorname) is not None

def get_sensor_id(db, sensorname):
    row = db.execute('SELECT id FROM sensor WHERE sensorname = ?', (sensorname,)).fetchone()
    return row['id'] if row is not None else None
