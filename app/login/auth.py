# app/login/auth.py

from functools import wraps
from flask import request, make_response, render_template, redirect, url_for, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from ..models import User
from .. import amivapi


def no_oauth(f):
    """
    Prevent redirect to OAuth provider.
    
    Shows an error 403 page instead.
    This decorator must be listed before @login_required!
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 302:
            abort(403)
        return response
    return wrapped


@login_manager.request_loader
def load_user_from_request(request):
    access_token = request.args.get('access_token')
    if access_token:
        try:
            response = amivapi.get('/sessions/{}'.format(access_token), token=access_token)
            data = response.json()
            user = User(data['_id'], access_token)
            login_user(user)
            return user
        except:
            return None
    return None

@login_manager.user_loader
def load_user_from_session(session_token):
    try:
        response = amivapi.get('/sessions/{}'.format(session_token), token=session_token)
        data = response.json()
        user = User(data['_id'], session_token)
        app.logger.info(user)
        return user
    except:
        return None
    return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Handles what to do when an unauthorized user tries to
    access a secured resource.

    This function handles the redirect to the OAuth provider.
    """
    if request.args.get('access_token'):
        # User does not have enough permissions
        abort(403)

    # redirect to OAuth provider
    client_id = app.config.get('OAUTH_CLIENT_ID')
    redirect_uri = request.url
    path = '/oauth?response_type=token&client_id={}&redirect_uri={}'.format(client_id, redirect_uri)
    return redirect(app.config.get('AMIV_API_URL') + path)
