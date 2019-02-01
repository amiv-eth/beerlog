# app/login/auth.py

import json
from functools import wraps
from flask import request, redirect, abort
from flask_login import login_required, login_user, logout_user
from app import app, login_manager
from ..models import User, ApiKey
from .. import amivapi


def apikey_required(f):
    """
    Requires to have a valid API key set in the Authorization header.

    This is a wrapper for the @login_required decorator.

    Error 401: shown when the Authorization header is missing.
    Error 403: shown when the provided Authorization header is invalid.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if ('Authorization' not in request.headers):
            abort(401)
        response = login_required(f)(*args, **kwargs)
        if response.status_code == 302:
            abort(403)
        return response
    return wrapped


def oauth_required(f):
    """
    Requires that the user is logged in with OAuth.

    This is a wrapper for the @login_required decorator.

    Error 403: shwon if trying to access with an api key (Authorization header).
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'Authorization' in request.headers:
            abort(403)
        return login_required(f)(*args, **kwargs)
    return wrapped


def load_trusted_user_from_api(token):
    """
    Returns a User instance for a trusted api user

    Returns None if the user session does not exist or the
    user is not in a trusted group.
    """
    session_response = amivapi.get('/sessions/{}'.format(token), token=token)

    if session_response.status_code != 200:
        return None

    session = session_response.json()
    query = json.dumps({'user': session['user'], 'group': { "$in": app.config.get('AMIV_API_TRUSTED_GROUPS') } })
    group_response = amivapi.get('/groupmemberships?where={}'.format(query), token=token)

    if group_response.status_code != 200 or len(group_response.json()['_items']) == 0:
        return None

    return User(session=session)

@login_manager.request_loader
def load_user_from_request(request):
    if 'access_token' in request.args:
        access_token = request.args.get('access_token')
        try:
            user = load_trusted_user_from_api(access_token)
            if not user:
                return None
            login_user(user)
            return user
        except:
            return None
    elif 'Authorization' in request.headers:
        authorization = request.headers.get('Authorization')
        try:
            apikey = ApiKey.query.filter_by(token=authorization).one()
            user = User(apikey=apikey)
            return user
        except:
            return None
    return None


@login_manager.user_loader
def load_user_from_session(session_token):
    try:
        user = load_trusted_user_from_api(session_token)
        if not user:
            return None
        return user
    except:
        return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    Handles what to do when an unauthorized user tries to
    access a secured resource.

    This function handles the redirect to the OAuth provider.
    """
    if 'access_token' in request.args:
        # User does not have enough permissions
        abort(403)

    # logout user in case the api session has been deleted.
    logout_user()

    # redirect to OAuth provider
    client_id = app.config.get('OAUTH_CLIENT_ID')

    redirect_uri = app.config.get('OAUTH_OWN_URL') + request.full_path
    path = '/oauth?response_type=token&client_id={}&redirect_uri={}'.format(client_id, redirect_uri)
    return redirect(app.config.get('AMIV_API_URL') + path)
