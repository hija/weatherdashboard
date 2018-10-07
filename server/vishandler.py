from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from server.db import get_db
from server.util import station_exists

bp = Blueprint('visualiations', __name__, url_prefix='/visualisations')

@bp.route('/')
def getstations():
    return render_template('vis/default.html')
