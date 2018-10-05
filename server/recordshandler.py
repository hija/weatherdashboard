from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from server.db import get_db

bp = Blueprint('records', __name__, url_prefix='/records')

@bp.route('/add', methods=('GET', 'POST'))
def addstation():
    return 'todo'
