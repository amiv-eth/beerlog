# app/amivapi.py
from flask import current_app as app
import requests

def get(path, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.get(app.config.get('AMIV_API_URL') + path, **kwargs, auth=requests.auth.HTTPBasicAuth(token, ''))

def post(path, data, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.get(app.config.get('AMIV_API_URL') + path, **kwargs, data=data, auth=requests.auth.HTTPBasicAuth(token, ''))

def delete(path, data, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.delete(app.config.get('AMIV_API_URL') + path, **kwargs, data=data, auth=requests.auth.HTTPBasicAuth(token, ''))
