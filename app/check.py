# app/amivapi.py

import requests
from datetime import date
from sqlalchemy import Date, cast, func
from . import app, db, amivapi
from .models import ProductReport
from .models.enums import ProductEnum, OrganisationEnum


def get_product_amounts(user, organisation):
    """Collects consumption statistics and calculates remaining free drinks."""
    max_available = get_max_available_free_products(user, organisation)
    consumed = get_consumed_products_today(user, organisation)
    available = {}

    for product in ProductEnum:
        available[product.value] = max(0, max_available.get(product.value, 0) - consumed.get(product.value, 0))

    return (available, consumed, max_available)


def get_available_free_products(user, organisation):
    """Get remaining free drinks based on user and organisation."""
    (available, _, _) = get_product_amounts(user, organisation)
    return available


def get_max_available_free_products(user, organisation):
    """Get the max number of available drinks for a user."""
    max_amount = 0

    if organisation == OrganisationEnum.AMIV:
        # Normal members have 1 free item per day
        if (user['membership'] is not 'none'):
            max_amount = 1
        
        # Special groups have 5 free items per day
        groupmemberships = amivapi.get_selected_groupmemberships(user, app.config.get('AMIV_API_PRIVILEGED_GROUPS'))
        if len(groupmemberships) > 0:
            max_amount = 5

    available = {}
    for product in ProductEnum:
        available[product.value] = max_amount
    return available


def get_consumed_products_today(user, organisation):
    """Get number of consumed products today."""
    consumed = {}
    for product in ProductEnum:
        consumed[product.value] = get_consumed_amount_by_product_today(user, organisation, product)
    return consumed


def get_consumed_amount_by_product_today(user, organisation, product):
    """Get number of consumed products of a given product today."""
    return db.session \
        .query(func.count(ProductReport._id).label('count')) \
        .filter(ProductReport.organisation == organisation) \
        .filter(ProductReport.product == product) \
        .filter(cast(ProductReport.timestamp,Date) == date.today()) \
        .scalar()
