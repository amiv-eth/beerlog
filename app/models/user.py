# app/models/user.py

from flask_login import UserMixin


class OAuthUser(UserMixin):
    """
    A user object representing a user authenticated with OAuth.

    :param str session: session object received from AMIV API

    """
    def __init__(self, session):
        self.id = session.user
        self.session = session

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user token to satisfy Flask-Login's requirements."""
        return self.session.token


class ApiKeyUser(UserMixin):
    """A user object representing a user authenticated by an api key.

    :param str apikey: apikey object loaded from database

    """
    def __init__(self, apikey):
        self.id = apikey._id
        self.apikey = apikey

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the apikey token to satisfy Flask-Login's requirements."""
        return self.apikey.token
