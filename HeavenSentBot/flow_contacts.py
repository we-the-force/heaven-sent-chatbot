from flask import session
from . import logout
from .db import _get_contacts

def flow_contact():
    user_id = session.get('user_id',0)
    if user_id != 0:
        contacts = _get_contacts(user_id)
        if len(contacts) > 0:
            message = ("Los siguientes contactos compartieron memorias contigo:\n")
            for c in contacts:
                message += ('- {name}\n'.format_map(c['owner']))
            message += ("Manda un mensaje con el nombre del contacto para recibir una memoria.")
            session['contacts'] = contacts
            session['thread'] = 'memories'
        else:
            message = ("No te han compartido ninguna memoria")
    else:
        message = logout.logout()
    return message