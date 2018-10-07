
def station_exists(db, stationname):
    return get_station_id(db, stationname) is not None

def get_station_id(db, stationname):
    row = db.execute('SELECT id FROM station WHERE stationname = ?', (stationname,)).fetchone()
    return row['id'] if row is not None else None
