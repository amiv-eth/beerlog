# app/error/views.py

from flask import render_template

from .. import app


@app.errorhandler(401)
def page_unauthorized(e):
    return render_template('error/401.html', title='Unauthorized'), 401


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('error/403.html', title='Forbidden'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html', title='Page not found'), 404


@app.errorhandler(500)
def page_server_error(e):
    return render_template('error/500.html', title='Internal Server Error'), 500
