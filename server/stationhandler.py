from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db

bp = Blueprint('stations', __name__, url_prefix='/stations')

@bp.route('/add', methods=('GET', 'POST'))
def addstation():
    if request.method == 'POST':
        if 'stationname' in request.form and 'description' in request.form:
            stationname = request.form['stationname']
            description = request.form['description']
            db = get_db()
            db.execute(
            'INSERT INTO station (stationname, description) VALUES (?, ?)',
            (stationname, description))
            db.commit()
            return 'Added Station!'
        else:
            return 'Missing parameters!'
    return 'This method requires an POST-Request with the fields stationname and description'

@bp.route('/list')
def getstations():
    db = get_db()
    stations = db.execute(
        'SELECT id, stationname, description'
        ' FROM station'
    ).fetchall()
    return render_template('stationlist.html', stations=stations)
