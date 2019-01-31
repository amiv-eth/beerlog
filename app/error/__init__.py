# app/error/__init__.py

from flask import Blueprint

error_bp = Blueprint('error', __name__)

from . import views
