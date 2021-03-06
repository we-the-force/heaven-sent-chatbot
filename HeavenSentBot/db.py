import requests
import json

from flask import current_app
from .helpers import _phone

def _url(path):
    return current_app.config['DATABASE'] + path

def _get(path):
    get_data = requests.get(_url(path))
    return json.loads(get_data.text)

def _get_user(number, x=0):
    if x == 2:
        return False
    if number[0] == '+':
        format_tel = 'INT' if x else 'NAT'
        number = _phone(format_tel, number)
    else:
        x = 1
    user_json = _get('/users/?mobile={0}'.format(number))
    if len(user_json) <= 0:
        return _get_user(number, x + 1)
    return user_json

def _get_contacts(userID):
    contacts = _get('/contacts?contact.id={0}'.format(userID))
    return contacts

def _get_memories(userID, ownerID):
    memories = _get('/memories?on_demand=true&sent=true&owners.id={}&recipients.id={}'.format(ownerID,userID))
    return memories
