# app/beerlog/views.py

from flask import render_template, make_response

from ..login import auth

from . import beerlog_bp


@beerlog_bp.route('/')
@auth.oauth_required
def home():
    """
    Handle requests to the / route
    """
    # load beerlog.home template
    return make_response(render_template('beerlog/list.html', title='Overview'))
