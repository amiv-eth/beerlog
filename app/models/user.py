# app/models/user.py

from flask_login import UserMixin


class User(UserMixin):
    """A user object representing the authenticated user.

    :param str id: user id ()
    :param str token: encrypted password for the user

    """
    def __init__(self, id, token=None):
        self.id = id
        self.token = token

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the user token to satisfy Flask-Login's requirements."""
        return self.token
