# app/api/views.py

from flask import make_response, request, abort, jsonify
from flask_login import current_user

from .. import app, db, amivapi
from ..check import get_available_free_products
from ..login import auth
from ..models import User, ProductReport
from ..models.enums import ProductEnum, OrganisationEnum

from . import api_bp


@api_bp.route('/check/<rfid>', methods = ['GET'])
@auth.apikey_required
def check(rfid=None):
    """
    Handle requests to the /check/<rfid> route
    """
    # validate parameters
    user = amivapi.get_user_by_rfid(rfid)
    if not user: abort(404)
    available = get_available_free_products(user, OrganisationEnum.AMIV)
    if not available: abort(500)

    # check permission and filter response values accordingly
    response = {}
    for permission in current_user.apikey.permissions:
        key = permission.product.value
        if key in available:
            response[key] = available.get(key, 0)

    return make_response(jsonify(response), 200)


@api_bp.route('/report', methods = ['POST'])
@auth.apikey_required
def report():
    """
    Handle requests to the /report route
    """
    data = request.get_json()
    issues = {}
    organisation = None
    product = None

    # Validate POST data
    if not data or not data.get('rfid'):
        issues['rfid'] = 'value must not be null or empty'

    if not data or not data.get('organisation'):
        issues['organisation'] = 'value must not be null or empty'
    else:
        label = data.get('organisation')
        organisation = OrganisationEnum.from_str(label)
        if organisation == None:
            issues['organisation'] = 'unallowed value {}'.format(label)

    if not data or not data.get('product'):
        issues['product'] = 'value must not be null or empty'
    else:
        label = data.get('product')
        product = ProductEnum.from_str(label)
        if product == None:
            issues['product'] = 'unallowed value {}'.format(label)

    if len(issues) > 0:
        abort(422, issues)

    # Check permissions
    if not check_permissions(product):
        abort(403, 'You don\'t have the permission to create the desired resource.')

    apiuser = amivapi.get_user_by_rfid(data.get('rfid'))
    user = apiuser['_id']
    if not user:
        user = data.get('rfid')

    report = ProductReport()
    report.user = user
    report.organisation = organisation
    report.product = product

    if (organisation == OrganisationEnum.AMIV):
        if not apiuser:
            issues['rfid'] = 'invalid value {}'.format(data.get('rfid'))
            abort(422, issues)

        # check if free drinks are available
        available = get_available_free_products(apiuser, organisation)
        if available.get(product.value, 0) == 0:
            abort(403, 'Free amount of {} used up'.format(product.value))

    db.session.add(report)
    db.session.commit()

    return make_created()


def check_permissions(product):
    """Check permissions for the current user."""
    if current_user.has_apikey():
        for permission in current_user.apikey.permissions:
            app.logger.info('product: {} | permission: {}'.format(product, permission.product))
            if permission.product == product:
                return True
    return False


def make_created():
    """Prepare created response."""
    return make_response(jsonify({"_status": "OK"}), 201)


@api_bp.errorhandler(401)
def page_unauthorized(e):
    if (e.description):
        description = e.description
    else:
        description = 'The server could not verify that you are authorized to access the ' \
            'URL requested. You either supplied the wrong credentials (e.g. a bad password), ' \
            'or your browser doesn\'t understand how to supply the credentials required.'

    return jsonify({
        '_status': 'ERR',
        '_error': {
            'code': 401,
            'message': description,
        }
    }), 401


@api_bp.errorhandler(403)
def page_forbidden(e):
    return jsonify({
        '_status': 'ERR',
        '_error': {
            'code': 403,
            'message': e.description,
        }
    }), 403


@api_bp.route("<path:invalid_path>")
def dummy_page(invalid_path):
    abort(404)


@api_bp.errorhandler(404)
def page_not_found(e):
    return jsonify({
        '_status': 'ERR',
        '_error': {
            'code': 404,
            'message': e.description,
        }
    }), 403


@api_bp.errorhandler(422)
def page_unprocessable(e):
    return jsonify({
        '_status': 'ERR',
        '_issues': e.description,
        '_error': {
            'code': 422,
            'message': 'Insertion failure: document contains error(s)',
        }
    }), 401


@api_bp.errorhandler(500)
def page_internal_error(e):
    return jsonify({
        '_status': 'ERR',
        '_error': {
            'code': 500,
            'message': e.description,
        }
    }), 500
