# app/beerlog/views.py

from flask import render_template, make_response, request
from sqlalchemy import Date, cast, func, desc
from datetime import datetime

from ..login import auth
from ..amivapi import get_users_by_ids, get_user_by_nethz, get_user_by_rfid
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

    ranking_query = db.session.query(
        func.count(ProductReport._id).label('consumption'),
        ProductReport.organisation,
        ProductReport.user,
        func.dense_rank().over(
            order_by=desc(func.count(ProductReport._id))
        ).label('rank')
    )

    organisation_query = db.session.query(
        func.count(ProductReport._id).label('consumption'),
        ProductReport.organisation,
        func.dense_rank().over(
            order_by=desc(func.count(ProductReport._id))
        ).label('rank')
    )

    user = None

    if request.args.get('user'):
        try:
            user = request.args.get('user')
            filterForm.user.process_data(user)

            # Check user with our member database
            apiUser = get_user_by_nethz(user)
            if (apiUser == None):
                apiUser = get_user_by_rfid(user)

            if (apiUser != None):
                user = apiUser['_id']
        except:
            pass
    if request.args.get('date_from'):
        try:
            date_from = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d').date()
            filterForm.date_from.process_data(date_from)
            ranking_query = ranking_query.filter(cast(ProductReport.timestamp,Date) >= date_from)
            organisation_query = organisation_query.filter(cast(ProductReport.timestamp,Date) >= date_from)
        except:
            pass
    if request.args.get('date_to'):
        try:
            date_to = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d').date()
            filterForm.date_to.process_data(date_to)
            ranking_query = ranking_query.filter(cast(ProductReport.timestamp,Date) <= date_to)
            organisation_query = organisation_query.filter(cast(ProductReport.timestamp,Date) <= date_to)
        except:
            pass
    if request.args.get('organisation') and request.args.get('organisation') != 'None':
        organisation = OrganisationEnum.from_str(request.args.get('organisation'))
        if organisation:
            filterForm.organisation.process_data(organisation)
            ranking_query = ranking_query.filter(ProductReport.organisation == organisation)
    if request.args.get('product') and request.args.get('product') != 'None':
        product = ProductEnum.from_str(request.args.get('product'))
        if product:
            filterForm.product.process_data(product)
            ranking_query = ranking_query.filter(ProductReport.product == product)
            organisation_query = organisation_query.filter(ProductReport.product == product)

    page = request.args.get('page', 1)
    try:
        page = int(page)
    except ValueError:
        page = 1
    first_position = (page - 1)*30

    ranking_subquery = ranking_query \
        .group_by(ProductReport.user, ProductReport.organisation) \
        .subquery()
    ranking_query = db.session.query(ranking_subquery)

    if (user != None):
        ranking_query = ranking_query.filter(ranking_subquery.c.user == user)

    ranking_query_results = ranking_query \
        .group_by(ranking_subquery.c.consumption, ranking_subquery.c.organisation, ranking_subquery.c.user, ranking_subquery.c.rank) \
        .order_by(desc(ranking_subquery.c.consumption)) \
        .paginate(page, 30)
    consumption_query_results = organisation_query \
        .order_by(desc('consumption')) \
        .group_by(ProductReport.organisation) \
        .all()

    # Resolve users with API
    user_ids = []
    for item in ranking_query_results.items:
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
        render_template('beerlog/list.html', filterform=filterForm, consumption=consumption_query_results,
          ranking=ranking_query_results, users=userDict, first_position=first_position, title='Overview'))
