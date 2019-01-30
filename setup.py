"""
Adds an api key to the database
"""

import argparse
from app import app, db
from app.models import ApiKey, ApiKeyPermission
from app.models.enums import ProductEnum

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('-p', '--permission', action='append')
args = parser.parse_args()

# Create API Key
print('Creating API Key...')
with app.app_context():
    apikey = ApiKey()
    apikey.name = args.name
    for productLabel in args.permission:
        print('permission: {}'.format(productLabel))
        permission = ApiKeyPermission()
        product = ProductEnum.from_str(productLabel)

        if product == None:
            continue
        permission.product = product
        apikey.permissions.append(permission)
        db.session.add(permission)
    token = apikey.token
    db.session.add(apikey)
    db.session.commit()

print('The generated token is:\n\n            {}\n\n'.format(token))
