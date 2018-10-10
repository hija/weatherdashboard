from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import sensor_exists, get_sensor_id, get_all_sensors

bp = Blueprint('visualiations', __name__, url_prefix='/visualisations')

@bp.route('/')
def getsensors(limit = 100):
    db = get_db()
    records = db.execute(
        'SELECT timepoint, AVG(temperature) AS temperature, AVG(humidity) AS humidity, AVG(pressure) AS pressure FROM record GROUP BY strftime(\'%Y-%m-%dT%H:%M:00.000\', timepoint) ORDER BY timepoint DESC LIMIT ?',
        (limit, )
    ).fetchall()
    data = dict()
    data['temperature'] = [record['temperature'] for record in records]
    data['humidity'] = [record['humidity'] for record in records]
    data['pressure'] = [record['pressure'] for record in records]
    data['dates'] = [record['timepoint'] for record in records]
    return render_template('vis/grouped_vis.html', data=data, sensors = get_all_sensors(db))

@bp.route('/show/<string:sensorname>')
def get_vis_for_sensor(sensorname):
    return get_vis_for_sensor_and_limit(sensorname, 3)

@bp.route('/show/<string:sensorname>/<int:limit>')
def get_vis_for_sensor_and_limit(sensorname, limit):
    db = get_db()
    if sensor_exists(db, sensorname):
        records = db.execute(
            'SELECT timepoint, temperature, humidity, pressure FROM record WHERE sensor_id = ? ORDER BY timepoint DESC LIMIT ?',
            (get_sensor_id(db, sensorname), limit)
        ).fetchall()
        data = dict()
        data['temperature'] = [record['temperature'] for record in records]
        data['humidity'] = [record['humidity'] for record in records]
        data['pressure'] = [record['pressure'] for record in records]
        data['dates'] = [record['timepoint'] for record in records]
        return render_template('vis/sensor_vis.html', data=data)
    else:
        flash('The sensor does not exist!', 'error')
        return render_template('vis/default.html')
