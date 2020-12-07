from flask import session
from . import logout
from .db import _get_contacts
from .dictionaries import palabras

def flow_contact(x=None):
    user_id = session.get('user_id',0)
    if user_id != 0:
        contacts = _get_contacts(user_id)
        lang = session.get('lang', 'en')
        if len(contacts) > 0:
            message = ("{}\n".format(palabras[lang].get("you_are_contact")))
            new_contacts = []
            for c in contacts:
                new_contacts.append(c['owner'])
                message += ('- {name}\n'.format_map(c['owner']))
            message += ("{}\n".format(palabras[lang].get("send_contact_name")))
            session['contacts'] = new_contacts
            session['thread'] = 'memories'
        else:
            message = ("{}\n".format(palabras[lang].get("you_are_not_contact")))
    else:
        message = logout.logout()
    return message