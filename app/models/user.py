# app/models/user.py

from flask_login import UserMixin


class User(UserMixin):
    """
    A user object representing an authenticated user.

    :param str session: session object received from AMIV API
    :param str apikey: apikey object loaded from database

    """
    def __init__(self, session=None, apikey=None):
        self.apikey = apikey
        self.session = session

        if self.has_apikey():
            self.id = apikey._id
        else:
            self.id = session['user']


    def has_apikey(self):
        """True, when apikey is set."""
        return self.apikey is not None


    def is_active(self):
        """True, as all users are active."""
        return True


    def get_id(self):
        """Return the user id to satisfy Flask-Login's requirements."""
        if self.has_apikey():
            return self.apikey.token
        return self.session['token']
