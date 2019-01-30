# app/error/views.py

from flask import flash, redirect, render_template, url_for, request, abort, make_response, current_app as app
from flask_login import login_required, login_user, logout_user, current_user

from . import error_bp
from .. import app

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('error/unauthorized.html', title='Unauthorized'), 403
