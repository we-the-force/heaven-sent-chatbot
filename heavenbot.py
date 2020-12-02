from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests
import phonenumbers
import json

app = Flask(__name__)
app.secret_key = 'beZ}6EmDsU1RNICI!Q)4EWq%?_1/]h'


switch_phrases = {
    "ayuda": "aun estoy en desarrollo no puedo ayudarte u.u",
    "help": "Sorry, I'm not finished yet.\nCommands:\nHola\nHi\nAhoy\nBye\nMensajes compartidos conmigo",
    "hola": "Hola Amigo",
    "hi": "Hi friend",
    "ahoy": "Arrgh",
    "bye": "See you n.n",
}


def _logout(x,y):
    session.pop('user_id', None)
    session.pop('user_name', None)
    message = "logged out"
    return message


def _test(x,y):
    message = "waiting for memories"
    session.pop('thread', None)
    return message


def _return_phrases(arg):
    return switch_phrases.get(arg, "I can't understand you write 'Help' for more information")


def _contacts_memories(user, userId):
    contacts = _get('/contacts?contact.id={0}'.format(userId))
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


def _get_user(number, x=0):
    if x == 2:
        return False
    if number[0] == '+':
        format_tel = 'INT' if x else 'NAT'
        number = _phone(format_tel, number)
    else:
        x = 1
    user_json = _get('/users/?mobile={0}'.format(number))
    if len(user_json) <= 0:
        return _get_user(number, x + 1)
    return user_json


def _url(path):
    return 'https://api.heavensentnow.com' + path


def _get(path):
    get_data = requests.get(_url(path))
    return json.loads(get_data.text)


def _phone(type_format, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type_format == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


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
        thread = session.get('thread', income_msg.lower())
        func = switch_commands.get(thread, lambda x,y: _return_phrases(thread))
        message = func(session.get('user_name'),user_id)
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
