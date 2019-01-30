# app/login/__init__.py

import secrets
from flask import Blueprint

login_bp = Blueprint('login', __name__)

from . import views
