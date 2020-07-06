from flask import Flask, request, session
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests
import phonenumbers
import json

app = Flask(__name__)
app.secret_key = 'beZ}6EmDsU1RNICI!Q)4EWq%?_1/]h'


@app.route("/")
def hello():
    return "Ahoy World!"


@app.route("/user")
def return_files():
    res = requests.get(_url('/users/?mobile=8442590888'))
    data = json.loads(res.text)
    #exist = len(data) > 0
    #name = data[0]['name'] if exist > 0 else 'No user'
    return str(data)

@app.route("/session")
def session_storage():
    counter = session.get('counter', 0)
    counter += 1
    session['counter'] = counter

    return str(counter)

@app.route("/contact")
def return_contacts():
    #res = requests.get(_url('/contacts?contact.id=28'))
    res = requests.get(_url('/contacts'))
    data = json.loads(res.text)
    message = ("Hello {0}<br>".format('Alex'))
    for c in data:
        message += ('{name}<br>'.format_map(c['owner']))
    return str(message)


@app.route("/sms", methods=['POST'])
def sms_reply():
    trasmisor = request.form.get('From')
    number = trasmisor.split(':')

    # busca el usuario por el telefono sin codigo del pais
    user_json = _get('/users/?mobile={0}'.format(_phone('NAT', number[1])))
    if len(user_json) <= 0:
        # busca el usuario por el telefono con codigo del pais
        user_json = _get('/users/?mobile={0}'.format(_phone('INT', number[1])))
        if len(user_json) <= 0:
            # no se encontro usuario
            user_json = False

    if user_json:
        # se encontro el usuario
        contacts = _get('/contacts?contact.id={0}'.format(user_json[0]['id']))
        #contacts = _get('/contacts?contact.id=28')
        message = ("Hello {0}\nThe following contacts have memories for you:\n".format(user_json[0]['name']))

        for c in contacts:
            message += ('{name}\n'.format_map(c['owner']))
        
        message += ("Use the contact's name in a message to receive one of their memories")
        
    else:
        # no hay usuario
        message = (
            "Sorry we did not find your user :C, if you do not have an account you can create one in Heaven Sent")
    # Create reply
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


def _url(path):
    return 'http://167.172.156.126:1337' + path


def _get(path):
    get_user = requests.get(_url(path))
    return json.loads(get_user.text)


def _phone(type, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


if __name__ == "__main__":
    app.run(port=3001, debug=True)
