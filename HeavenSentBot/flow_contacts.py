from flask import session
from . import logout
from .db import _get_contacts

def flow_contact(x=None):
    user_id = session.get('user_id',0)
    if user_id != 0:
        contacts = _get_contacts(user_id)
        if len(contacts) > 0:
            message = ("Eres contacto de los siguientes usuarios:\n")
            new_contacts = []
            for c in contacts:
                new_contacts.append(c['owner'])
                message += ('- {name}\n'.format_map(c['owner']))
            message += ("Manda un mensaje con el nombre del usuario para recibir una memoria.")
            session['contacts'] = new_contacts
            session['thread'] = 'memories'
        else:
            message = ("No eres contacto de ningun usuario")
    else:
        message = logout.logout()
    return message