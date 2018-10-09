from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import sensor_exists

bp = Blueprint('sensors', __name__, url_prefix='/sensors')

@bp.route('/add', methods=('GET', 'POST'))
def addsensor():
    if request.method == 'POST':
        if 'sensorname' in request.form and 'description' in request.form:
            sensorname = request.form['sensorname']
            if '/' in sensorname:
                return 'Invalid sensorname'
            description = request.form['description']
            db = get_db()
            if sensor_exists(db, sensorname):
                return 'sensor already exists!'
            db.execute(
            'INSERT INTO sensor (sensorname, description) VALUES (?, ?)',
            (sensorname, description))
            db.commit()
            return 'Added sensor!'
        else:
            return 'Missing parameters!'
    return 'This method requires an POST-Request with the fields sensorname and description'

@bp.route('/')
def getsensors():
    db = get_db()
    sensors = db.execute(
        'SELECT id, sensorname, description'
        ' FROM sensor'
    ).fetchall()
    return render_template('sensor/sensorlist.html', sensors=sensors)

@bp.route('/delete/<string:sensorname>')
def delete_sensor(sensorname):
    db = get_db()
    if sensor_exists(db, sensorname):
        db.execute('DELETE FROM sensor WHERE sensorname = ?', (sensorname,))
        db.commit()
        return 'Deleted: {}'.format(sensorname)
    else:
        return 'sensor does not exist!'
