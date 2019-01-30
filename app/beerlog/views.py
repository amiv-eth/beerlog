# app/login/views.py

from flask import render_template, make_response
from flask_login import login_required

from . import beerlog_bp


@beerlog_bp.route('/')
@login_required
def home():
    """
    Handle requests to the / route
    """
    # load beerlog.home template
    return make_response(render_template('beerlog/list.html', title='Overview'))
