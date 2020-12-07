from flask import session
from .dictionaries import palabras

def logout():
    lang = session.get('lang', 'en')
    message = ("{}".format(palabras[lang].get("logout")))
    session.clear()
    return message