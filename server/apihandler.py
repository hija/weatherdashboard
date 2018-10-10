from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from server.db import get_db
from server.util import sensor_exists, get_sensor_id

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/add', methods=('GET', 'POST'))
def addrecord():
    if request.method == 'POST':
        if 'sensorname' in request.form:
            sensorname = request.form['sensorname']
            db = get_db()
            if sensor_exists(db, sensorname):
                # INSERT
                temperature = request.form.get('temperature', 'NULL')
                humidity = request.form.get('humidity', 'NULL')
                air_pressure = request.form.get('air_pressure', 'NULL')
                db.execute('INSERT INTO record (sensor_id, temperature, humidity, pressure) VALUES (?, ?, ?, ?)',
                (get_sensor_id(db, sensorname), temperature, humidity, air_pressure))
                db.commit()
                return 'Inserted'
            else:
                return 'Sensor does not exist'
        else:
            return 'Staionname not found in POST-Request'
    return 'This method requires a POST-Request'
