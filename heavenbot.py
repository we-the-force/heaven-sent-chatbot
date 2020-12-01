from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests
import phonenumbers
import json

app = Flask(__name__)
app.secret_key = 'beZ}6EmDsU1RNICI!Q)4EWq%?_1/]h'

switch_phrases = {
    "Ayuda": "aun estoy en desarrollo no puedo ayudarte u.u",
    "Help": "Sorry, I'm not finished yet.\nCommands:\nHola\nHi\nAhoy\nBye",
    "Hola": "Hola Amigo",
    "Hi": "Hi friend",
    "Ahoy": "Arrgh",
    "Bye": "See you n.n"
}

@app.route("/")
def hello():
    return 'Hello'

@app.route("/session")
def session_storage():
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter
    return str(counter)

@app.route("/sms", methods=['POST'])
def sms_reply():
    income_msg = request.form.get('Body')
    user_id = session.get('user_id', 0)

    if user_id != 0:
        #user_name = session.get('user_name')
        message = _return_phrases(income_msg)
    else:
        trasmisor = request.form.get('From')
        number = trasmisor.split(':')

        # busca el usuario por el telefono
        user_json = _get_user(number[1])

        if user_json:

            session['user_id'] = user_json[0]['id']
            session['user_name'] = user_json[0]['name']
            # se encontro el usuario
            contacts = _get(
                '/contacts?contact.id={0}'.format(session['user_id']))
            #contacts = _get('/contacts?contact.id=28')
            message = ("Hello {0}\n".format(session['user_name']))
            if len(contacts) > 0:
                message += ("The following contacts have memories for you:\n")
                for c in contacts:
                    print(len(c))
                    message += ('{name}\n'.format_map(c['owner']))
                message += ("Use the contact's name in a message to receive one of their memories")
            else:
                message += ("You have not been shared any memory")

        else:
            # no hay usuario
            message = (
                "Sorry we did not find your user :C, if you do not have an account you can create one in Heaven Sent")

    # Create reply
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


def _return_phrases(arg):
    return switch_phrases.get(arg, "I can't understand you write 'Help' for more information")


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


if __name__ == "__main__":
    app.run(port=3001, debug=True)
