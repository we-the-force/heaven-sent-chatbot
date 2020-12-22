import random
import json
from flask import session
from .db import _get_memories, _url
from .dictionaries import memories_messages, memories_pictures, palabras
from .helpers import flow_menu

from .natural_language_processing import normalize, tokenize


def flow_memory(income):
    contacts = session.get('contacts', [])
    in_flow = session.get('memory', 0)
    if len(contacts) > 0:
        if in_flow != 0:
            msg = flow_get_memory(income, in_flow)
        else:
            msg = flow_ask_memory(income, contacts)
    else:
        # aqui no deberia poder entrar
        lang = session.get('lang', 'en')
        msg = ("{}".format(palabras[lang].get("can_not_find")))
        session.pop('contacts')
        session.pop('memory', None)
        session.pop('thread')
    return msg


def flow_get_memory(income, ownerID):
    message = 0
    picture = 0
    for x in memories_messages:
        if x in income:
            message = 1
            break

    if not(message):
        for x in memories_pictures:
            if x in income:
                picture = 1
                break

    memory = _get_memories(session.get('user_id'), ownerID)
    msg = ""
    if len(memory) > 0:
        memory = random.choice(memory)

        if message:
            msg = format_message(memory)
        elif picture:
            msg = format_picture(memory)
        else:
            if random.choice([True, False]):
                msg = format_message(memory)
            else:
                msg = format_picture(memory)
    else:
        lang = session.get('lang', 'en')
        msg = ("{}".format(palabras[lang].get("no_memory_shared")))
        msg += flow_menu()

    session.pop('contacts')
    session.pop('memory',None)
    session.pop('thread')
    return msg


def flow_ask_memory(income, contacts):
    ownerID = 0
    ownerName = ""
    for x in contacts:
        name = x['name'].lower()
        contacto = tokenize(name)
        result = all(elem in income for elem in contacto)
        if result:
            ownerID = x['id']
            ownerName = x['name'].lower()
            break

    lang = session.get('lang', 'en')

    if ownerID != 0:
        if lang == 'en':
            msg = ("Would you like a message or a photo from {}?".format(ownerName))
        else:
            msg = ("¿Te gustaria un mensaje o una imagen de {}?".format(ownerName))
        session['memory'] = ownerID
    else:
        msg = ("{}".format(palabras[lang].get("can_not_find")))
        session.pop('contacts')
        session.pop('memory',None)
        session.pop('thread')

    return msg


def format_message(memoria):
    title = memoria.get('title')
    description = memoria.get('description')
    msg = ("{}\n".format(title))
    msg += ("{}\n".format(description))
    return msg


def format_picture(memoria):
    cover = memoria.get('cover').get('url')
    mediaURLs = []
    mediaURLs.append(cover)
    for x in memoria['media']:
        mediaURLs.append(x['url'])

    url = _url(random.choice(mediaURLs))
    resp = ['media',url]
    return resp
