# app/login/auth.py

from functools import wraps
from flask import request, redirect, abort
from flask_login import login_required, login_user, logout_user
from app import app, login_manager
from ..models import OAuthUser, ApiKeyUser, ApiKey
from .. import amivapi


def apikey_required(f):
    """
    Requires to have a valid API key set in the Authorization header.

    Shows an error 403 page if unauthorized.
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

    Shows an error 403 page if one tries to access with an api key.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'Authorization' in request.headers:
            abort(403)
        return login_required(f)(*args, **kwargs)
    return wrapped


@login_manager.request_loader
def load_user_from_request(request):
    if 'access_token' in request.args:
        access_token = request.args.get('access_token')
        try:
            response = amivapi.get('/sessions/{}'.format(access_token), token=access_token)
            session = response.json()
            user = OAuthUser(session)
            login_user(user)
            return user
        except:
            return None
    elif 'Authorization' in request.headers:
        authorization = request.headers.get('Authorization')
        try:
            apikey = ApiKey.query(token=authorization).one()
            user = ApiKeyUser(apikey)
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
    redirect_uri = request.url
    path = '/oauth?response_type=token&client_id={}&redirect_uri={}'.format(client_id, redirect_uri)
    return redirect(app.config.get('AMIV_API_URL') + path)
