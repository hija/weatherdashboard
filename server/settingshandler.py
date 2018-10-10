from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import sensor_exists, get_sensor_id

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
    import random
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
        from time import strftime, localtime
        import datetime

        for sensor in sensors:
            _time = datetime.datetime.now()
            sensor_id = get_sensor_id(db, sensor)
            temperature = random.randint(20, 35)
            humidity = random.random()
            pres = random.randint(900, 1500)
            for i in range(10):
                temperature = temperature + random.uniform(-5, 5)
                humidity = humidity + random.uniform(-0.1, 0.1)
                pres = pres + random.uniform(-10, 10)
                _time = _time - datetime.timedelta(minutes = 10)

                # sanity checks
                if humidity > 1:
                    humidity = 1
                elif humidity < 0:
                    humidity = 0

                db.execute('INSERT INTO record (sensor_id, temperature, humidity, pressure, timepoint) VALUES (?, ?, ?, ?, ?)',
                (sensor_id, temperature, humidity, pres, _time))
            db.commit()

    sensors = generate_dummy_sensors()
    generate_dummy_entries(sensors)
    flash('The dummy entries have been generated', 'success')
    return render_template('settings/default.html')
