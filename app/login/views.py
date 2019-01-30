# app/login/views.py

from flask import flash, redirect, render_template, url_for, request, abort, make_response
from flask_login import login_required, login_user, logout_user, current_user

from . import login_bp

@login_bp.route('/logout')
def logout():
    """
    Handle requests to the /logout route
    """
    authenticated = current_user.is_authenticated
    logout_user()

    if authenticated:
        return make_response(render_template('login/logout.html', title='Logout'))
    return redirect(url_for('beerlog.home'))
