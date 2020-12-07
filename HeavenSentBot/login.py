from flask import session
from .db import _get_user
from .flow_contacts import flow_contact
from .helpers import flow_menu

def login(number):
    user_json = _get_user(number)
    if user_json:
        session['user_id'] = user_json[0]['id']
        session['user_name'] = user_json[0]['name']
        message = ('Hola {} bienvenido al servicio on demand de HeavenSent.\nPara comenzar, seleccione la opción que mejor satisface lo que buscas:\n'.format(user_json[0]['name']))
        message += flow_menu()
    else:
        message = ("Lo siento, no te encontramos en nuestro sistema.\nSi no tienes una cuenta puedes crear una en app.heavensentnow.com")
    return message
