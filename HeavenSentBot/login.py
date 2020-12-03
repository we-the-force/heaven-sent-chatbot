from flask import session
from .db import _get_user
from .flow_contacts import flow_contact

def login(number):
    user_json = _get_user(number)
    if user_json:
        session['user_id'] = user_json[0]['id']
        session['user_name'] = user_json[0]['name']
        message = ('Hola {} bienvenido a Heaven Sent \n'.format(user_json[0]['name']))
        session['thread'] = 'contacts'
        message += flow_contact()
    else:
        message = ("Lo siento no te encontramos en nuestro sistema :C, si no tienes una cuenta puedes crear una en app.heavensentnow.com")
    return message
