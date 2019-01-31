# app/beerlog/__init__.py

from flask import Blueprint

beerlog_bp = Blueprint('beerlog', __name__)

from . import views
