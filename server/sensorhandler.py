from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import sensor_exists
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

bp = Blueprint('sensors', __name__, url_prefix='/sensors')

### FORMS ####
class AddForm(FlaskForm):

    def valid_sensorname(form, field):
        import re
        from wtforms import ValidationError
        if re.search('[^a-z0-9_]+', field.data) is not None:
            raise ValidationError('Sensorname must be lowercase and underscores only!')

    name = StringField('Sensorname', validators=[DataRequired(), valid_sensorname])
    description = StringField('Description', validators=[DataRequired()])
##############

@bp.route('/add', methods=('GET', 'POST'))
def addsensor():
    form = AddForm()
    if form.validate_on_submit():
        db = get_db()
        if sensor_exists(db, form.name.data):
            flash(u'There is already a sensor with this name in the database!', 'error')
        else:
            db.execute(
                     'INSERT INTO sensor (sensorname, description) VALUES (?, ?)',
                     (form.name.data, form.description.data))
            db.commit()
            flash(u'The sensor {} has been sucessfully added to the database!'.format(form.name.data), 'success')
            return redirect(url_for('sensors.addsensor'))
    return render_template('sensor/add.html', form=form)

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
        flash(u'The sensor has been deleted!', 'success')
        return getsensors()
    else:
        flash(u'The sensor does not exist!', 'error')
        return getsensors()
