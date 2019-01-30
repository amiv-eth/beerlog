# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from werkzeug.contrib.fixers import ProxyFix

# db variable initialization
db = SQLAlchemy()

# get flask login manager
login_manager = LoginManager()

# initialize flask app and configure
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# initialize ORM
db.init_app(app)

# add login functionality from flask-login
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "beerlog.home"

# add database migration from flask-migrate
Migrate(app, db)

# add flask-bootstrap
Bootstrap(app)

# add all persistent data models
from app import models

# add all blueprints
from .login import login_bp
app.register_blueprint(login_bp)
from .error import error_bp
app.register_blueprint(error_bp)
from .beerlog import beerlog_bp
app.register_blueprint(beerlog_bp)
from .api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')
