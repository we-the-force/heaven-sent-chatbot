from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse
from src.helpers import _return_phrases
from src.db import _get_user, _get_contacts
import requests
import phonenumbers
import json

app = Flask(__name__)
app.secret_key = 'beZ}6EmDsU1RNICI!Q)4EWq%?_1/]h'


def _logout(x,y):
    session.pop('user_id', None)
    session.pop('user_name', None)
    message = "logged out"
    return message


def _test(x,y):
    message = "waiting for memories"
    session.pop('thread', None)
    return message


def _contacts_memories(user, userId):
    contacts = _get_contacts(userId)
    message = ("Hello {0}\n".format(user))
    if len(contacts) > 0:
        message += ("The following contacts have memories for you:\n")
        for c in contacts:
            message += ('- {name}\n'.format_map(c['owner']))
        message += ("Use the contact's name in a message to receive one of their memories")
        session['thread'] = 'waiting contact name'
    else:
        message += ("You have not been shared any memory")
    return message


switch_commands = {
    "salir": _logout,
    "mensajes compartidos conmigo": _contacts_memories
}


@app.route("/sms", methods=['POST'])
def sms_reply():
    #consigo el mensaje
    income_msg = request.form.get('Body')
    #consigo el id de session, si no hay lo pongo en zero
    user_id = session.get('user_id', 0)

    #si existe la session
    if user_id != 0:
        #thread = session.get('thread', income_msg.lower())
        #func = switch_commands.get(thread, lambda x,y: _return_phrases(thread))
        #message = func(session.get('user_name'),user_id)
        message = _return_phrases(income_msg)
    #si no existe session
    else:
        #de donde viene el mensaje
        trasmisor = request.form.get('From')
        #consigue el numero
        number = trasmisor.split(':')

        # busca el usuario por el telefono
        user_json = _get_user(number[1])

        #si hay usuario
        if user_json:
            session['user_id'] = user_json[0]['id']
            session['user_name'] = user_json[0]['name']
            message = _contacts_memories(
                session['user_name'], session['user_id'])

        else:
            # no hay usuario
            message = (
                "Sorry we did not find your user :C, if you do not have an account you can create one in app.heavensentnow.com")

    # Create reply
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(port=3001, debug=True)
