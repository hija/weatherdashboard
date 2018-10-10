from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import sensor_exists

bp = Blueprint('settings', __name__, url_prefix='/settings')

@bp.route('/')
def getsensors():
    return render_template('settings/default.html')

@bp.route('/about')
def getabout():
    return render_template('settings/about.html')

@bp.route('/reset_db', methods=("POST",))
def reset_db():
    from server.db import init_db
    init_db()
    flash('The database has been resetted!', 'success')
    return render_template('settings/default.html')

@bp.route('/generate_dummy_data', methods=("POST",))
def generate_dummy_data():
    from secrets import choice
    db = get_db()

    def generate_dummy_sensors():
        names = ['alan', 'adam', 'collin', 'ethan', 'frank', 'homer']
        rooms = ['garage', 'livingroom', 'kitchen', 'bath']
        extender = ['final', 'new', 'old']
        generated_sensors = []
        for i in range(10):
            generated_sensor = "{}_{}".format(choice(names), choice(rooms))
            while generated_sensor in generated_sensors:
                generated_sensor = "{}_{}".format(generated_sensor, choice(extender))
            generated_sensors.append(generated_sensor)
        for sensor in generated_sensors:
            db.execute('INSERT INTO sensor (sensorname, description) VALUES (?, "Dummy Sensor!")', (sensor, ))
        db.commit()
        return generated_sensors

    def generate_dummy_entries(sensors):
        for _ in range(10):
            pass
    sensors = generate_dummy_sensors()
    flash('The dummy entries have been generated', 'success')
    return render_template('settings/default.html')
