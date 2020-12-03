from flask import session
from .db import _get_user

def login(number):
    user_json = _get_user(number)
    if user_json:
        session['user_id'] = user_json[0]['id']
        session['user_name'] = user_json[0]['name']
        message = 'Mensaje de bienvenida'
        #send to flow 1
    else:
        message = ("Sorry we did not find your user :C, if you do not have an account you can create one in app.heavensentnow.com")
    return message
