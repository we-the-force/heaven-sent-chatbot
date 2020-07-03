from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests
import phonenumbers
import json

app = Flask(__name__)


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


@app.route("/contact")
def return_contacts():
    res = requests.get(_url('/contacts?contact.id=28'))
    data = json.loads(res.text)
    return str(data)


@app.route("/sms", methods=['POST'])
def sms_reply():
    #msg = request.form.get('Body')
    trasmisor = request.form.get('From')
    number = trasmisor.split(':')
    user_json = _get('/users/?mobile={0}'.format(_phone('NAT',number[1])))
    if len(user_json) <= 0:
        user_json = _get('/users/?mobile={0}'.format(_phone('INT',number[1])))
        if len(user_json) <= 0:
            user_json = False
    if user_json:
        message = ("It's a pleasure talking to you {0}, how can I help you ?".format(
            user_json[0]['name']))
    else:
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
    app.run(port=3000, debug=True)
