from flask import session
from .db import _get_user
from .flow_contacts import flow_contact
from .helpers import flow_menu
from .dictionaries import palabras

def login(number):
    user_json = _get_user(number)
    lang = session.get('lang', 'en')
    if user_json:
        session['user_id'] = user_json[0]['id']
        session['user_name'] = user_json[0]['name']
        if lang == 'en':
            message = ('Hi {}! Welcome to the on demand service of HeavenSent.\nTo start, please select the option that better suits your need:\n'.format(user_json[0]['name']))
        else:
            message = ('Hola {} bienvenido al servicio on demand de HeavenSent.\nPara comenzar, seleccione la opción que mejor satisface lo que buscas:\n'.format(user_json[0]['name']))
        message += flow_menu()
    else:
        message = ("{}".format(palabras[lang].get("user_not_found")))
    return message
