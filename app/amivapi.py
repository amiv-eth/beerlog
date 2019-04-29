# app/amivapi.py

import json
import requests
from . import app

def get(path, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.get(app.config.get('AMIV_API_URL') + path, **kwargs, headers={'Authorization': token, 'Content-Type': 'application/json'})


def post(path, data, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.get(app.config.get('AMIV_API_URL') + path, **kwargs, data=data, headers={'Authorization': token, 'Content-Type': 'application/json'})


def delete(path, data, token=None, **kwargs):
    if token == None:
        token = app.config.get('AMIV_API_KEY')
    return requests.delete(app.config.get('AMIV_API_URL') + path, **kwargs, data=data, headers={'Authorization': token, 'Content-Type': 'application/json'})

def get_users_by_ids(ids, token=None):
    query = json.dumps({ "_id": { "$in": ids } })
    response = get('/users?max_results=' + str(len(ids)) + '&where=' + query, token)
    data = response.json()
    if response.status_code == 200:
        return data['_items']
    return []

def get_user_by_nethz(nethz, token=None):
    if (nethz is not None):
        response = get('/users?where={"nethz":"' + nethz + '"}', token)
        data = response.json()
        if response.status_code == 200 and data['_meta']['total'] == 1:
            return data['_items'][0]
    return None

def get_user_by_rfid(rfid, token=None):
    if (rfid is not None):
        response = get('/users?where={"rfid":"' + rfid + '"}', token)
        data = response.json()
        if response.status_code == 200 and data['_meta']['total'] == 1:
            return data['_items'][0]
    return None

def get_selected_groupmemberships(user, groups=[], token=None):
    query = json.dumps({"user": user['_id'], "group": { "$in": groups } })
    response = get('/groupmemberships?where=' + query, token)
    data = response.json()
    if response.status_code == 200:
        return data['_items']
    return []
