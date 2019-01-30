"""
Adds an api key to the database
"""

import argparse
from app import app, db
from app.models import ApiKey, ApiKeyPermission
from app.models.enums import BeverageTypeEnum

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
    for param in args.permission:
        print('permission: {}'.format(param))
        permission = ApiKeyPermission()
        if param == 'beer':
            permission.beverage_type = BeverageTypeEnum.BEER
        elif param == 'coffee':
            permission.beverage_type = BeverageTypeEnum.COFFEE
        else:
            continue
        apikey.permissions.append(permission)
        db.session.add(permission)
    token = apikey.token
    db.session.add(apikey)
    db.session.commit()

print('The generated token is:\n\n            {}\n\n'.format(token))
