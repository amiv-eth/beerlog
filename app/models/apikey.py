# app/models/apikey.py

import secrets
from app import db
from .enums import BeverageTypeEnum, OrganisationEnum


class ApiKey(db.Model):
    """
    API keys for vending machines to access the provided API endpoints.
    """

    __tablename__ = 'apikeys'

    def __init__(self):
        self.token = secrets.token_urlsafe(22)

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(32), nullable=False, unique=True)
    permissions = db.relationship("ApiKeyPermission", lazy='joined')
    created = db.Column(db.DateTime, nullable=False, server_default=db.func.now())


class ApiKeyPermission(db.Model):
    """
    Api key permission entry
    
    This specifies for which beverage types, the key should have access.
    """

    __tablename__ = 'apikey_permissions'

    _id = db.Column(db.Integer, primary_key=True)
    apikey_id = db.Column(db.Integer, db.ForeignKey('{}._id'.format(ApiKey.__tablename__)))
    apikey = db.relationship('ApiKey', backref = ApiKey.__tablename__)
    beverage_type = db.Column(db.Enum(BeverageTypeEnum), nullable=False)