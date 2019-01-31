# app/beerlog/views.py

from flask import render_template, make_response, request
from sqlalchemy import Date, cast, func, desc
from datetime import datetime

from ..login import auth
from ..amivapi import get_users_by_ids
from ..models import ProductReport
from ..models.enums import OrganisationEnum, ProductEnum
from .. import app, db

from . import beerlog_bp
from .forms import FilterForm


@beerlog_bp.route('/')
@auth.oauth_required
def home():
    """
    Handle requests to the / route
    """
    filterForm = FilterForm()

    query = db.session \
        .query(func.count(ProductReport._id).label('consumption'), ProductReport.user, ProductReport.organisation) \
        .group_by(ProductReport.user, ProductReport.organisation) \
        .order_by(desc('consumption'))

    if request.args.get('date_from'):
        app.logger.info('date_from: {}'.format(request.args.get('date_from')))
        try:
            date_from = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d').date()
            filterForm.date_from.process_data(date_from)
            query = query.filter(cast(ProductReport.timestamp,Date) >= date_from)
        except:
            pass
    if request.args.get('date_to'):
        app.logger.info('date_to: {}'.format(request.args.get('date_to')))
        try:
            date_to = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d').date()
            filterForm.date_to.process_data(date_to)
            query = query.filter(cast(ProductReport.timestamp,Date) <= date_to)
        except:
            pass
    if request.args.get('organisation') and request.args.get('organisation') != 'None':
        app.logger.info('organisation: {}'.format(request.args.get('organisation')))
        organisation = OrganisationEnum.from_str(request.args.get('organisation'))
        if organisation:
            filterForm.organisation.process_data(organisation)
            query = query.filter(ProductReport.organisation == organisation)
    if request.args.get('product') and request.args.get('product') != 'None':
        app.logger.info('product: {}'.format(request.args.get('product')))
        product = ProductEnum.from_str(request.args.get('product'))
        if product:
            filterForm.product.process_data(product)
            query = query.filter(ProductReport.product == product)

    page = request.args.get('page', 1)
    query_results = query.paginate(page, 30)
    first_position = (page - 1)*30

    # Resolve users
    user_ids = []
    for item in query_results.items:
        if len(item.user) > 6:
            user_ids.append(item.user)

    users = get_users_by_ids(user_ids)
    userDict = {}
    for user in users:
        if user.get('nethz'):
            userDict[user.get('_id')] = user.get('nethz')
        else:
            userDict[user.get('_id')] = user.get('email')

    # load beerlog.home template
    return make_response(
        render_template('beerlog/list.html', filterform=filterForm, query_results=query_results,
          users=userDict, first_position=first_position, title='Overview'))
