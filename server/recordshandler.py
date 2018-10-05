from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from server.db import get_db
from server.stationhandler import station_exists

bp = Blueprint('records', __name__, url_prefix='/records')

@bp.route('/add', methods=('GET', 'POST'))
def addrecord():
    if request.method == 'POST':
        if 'stationname' in request.form:
            stationname = request.form['stationname']
            db = get_db()
            if station_exists(db, stationname):
                # INSERT
                return 'Todo: Insert'
            else:
                return 'Station does not exist'
    return 'This method requires an POST-Request with the field stationname'
