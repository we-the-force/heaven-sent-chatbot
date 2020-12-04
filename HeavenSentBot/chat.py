from flask import session
from .flow_contacts import flow_contact


def chatbot(x):
    if 'mensaje' in x:
        session['thread'] = 'contacts'
        msg = flow_contact()
    else:
        msg = "Aqui va a ir el chat bot pero por el momento si escrbies mensaje reinicio el flujo principal\n "
    return msg
