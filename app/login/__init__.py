
import secrets
from flask import Blueprint

from . import auth

login_bp = Blueprint('login', __name__)

from . import views
