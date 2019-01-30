# app/models/beverage.py

from app import db
from ..models.enums import ProductEnum, OrganisationEnum


class ProductReport(db.Model):
    """
    Product consumation log entry.
    """

    __tablename__ = 'product_reports'

    _id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128), nullable=False)
    organisation = db.Column(db.Enum(OrganisationEnum), nullable=False)
    product = db.Column(db.Enum(ProductEnum), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
