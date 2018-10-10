from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from server.db import get_db
from server.util import sensor_exists, get_sensor_id

bp = Blueprint('records', __name__, url_prefix='/records')

@bp.route('/<string:sensorname>')
def get_records_for_sensorname(sensorname):
    db = get_db()
    if sensor_exists(db, sensorname):
        records = db.execute(
            'SELECT id, timepoint, temperature, humidity, pressure FROM record WHERE sensor_id = ?', (get_sensor_id(db, sensorname),)
        ).fetchall()
        return render_template('record/recordlist.html', records=records)
    else:
        flash(u'The sensor does not exist. Showing all records instead!', 'error')
        return get_records()

@bp.route('/')
def get_records():
    db = get_db()
    records = db.execute(
        'SELECT record.id, sensor.sensorname, timepoint, temperature, humidity, pressure FROM record INNER JOIN sensor on record.sensor_id = sensor.id; '
    ).fetchall()
    return render_template('record/recordlist.html', records=records, showsensorname = True)
