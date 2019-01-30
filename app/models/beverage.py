# app/models/beverage.py

from app import db
from ..models.enums import BeverageTypeEnum, OrganisationEnum


class Beverage(db.Model):
    """
    Beverage consumation log entry.
    """

    __tablename__ = 'beverage_log'

    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False)
    organisation = db.Column(db.Enum(OrganisationEnum))
    beverage_type = db.Column(db.Enum(BeverageTypeEnum))
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
