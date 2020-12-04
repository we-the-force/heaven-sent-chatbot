import random
import json
from flask import session
from .db import _get_memories, _url
from .dictionaries import memories_messages, memories_pictures


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
        msg = "Lo siento no pude encontrar a ningun contacto. \n Escribe 'Help' para recibir ayuda."
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
        msg = "Lo sentimos el usuario no te ha compartido ninguna memoria"

    session.pop('contacts')
    session.pop('memory',None)
    session.pop('thread')
    return msg


def flow_ask_memory(income, contacts):
    ownerID = 0
    ownerName = ""
    for x in contacts:
        name = x['name'].lower()
        if name in income:
            ownerID = x['id']
            ownerName = x['name'].lower()
            break

    if ownerID != 0:
        msg = ("Te gustaria un mensaje o una imagen de {}?".format(ownerName))
        session['memory'] = ownerID
    else:
        msg = "Lo siento no pude encontrar a ningun contacto. \n Escribe 'Help' para recibir ayuda."
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
