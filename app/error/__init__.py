
import secrets
from flask import Blueprint

error_bp = Blueprint('error', __name__)

from . import views
