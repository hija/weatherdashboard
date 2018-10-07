from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from server.db import get_db
from server.util import station_exists, get_station_id

bp = Blueprint('records', __name__, url_prefix='/records')

@bp.route('/add', methods=('GET', 'POST'))
def addrecord():
    if request.method == 'POST':
        if 'stationname' in request.form:
            stationname = request.form['stationname']
            db = get_db()
            if station_exists(db, stationname):
                # INSERT
                temperature = request.form.get('temperature', 'NULL')
                humidity = request.form.get('humidity', 'NULL')
                air_pressure = request.form.get('air_pressure', 'NULL')
                db.execute('INSERT INTO record (station_id, temperature, humidity, pressure) VALUES (?, ?, ?, ?)',
                (get_station_id(db, stationname), temperature, humidity, air_pressure))
                db.commit()
                return 'Inserted'
            else:
                return 'Station does not exist'
        else:
            return 'Staionname not found in POST-Request'
    return 'This method requires a POST-Request'

@bp.route('/<string:stationname>')
def get_records_for_stationname(stationname):
    db = get_db()
    if station_exists(db, stationname):
        records = db.execute(
            'SELECT id, timepoint, temperature, humidity, pressure FROM record WHERE station_id = ?', (get_station_id(db, stationname),)
        ).fetchall()
        return render_template('record/recordlist.html', records=records)
    else:
        flash(u'The station does not exist. Showing all records instead!', 'error')
        return get_records()

@bp.route('/')
def get_records():
    db = get_db()
    records = db.execute(
        'SELECT record.id, station.stationname, timepoint, temperature, humidity, pressure FROM record INNER JOIN station on record.station_id = station.id; '
    ).fetchall()
    return render_template('record/recordlist.html', records=records, showstationname = True)
