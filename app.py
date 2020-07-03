from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import requests
import phonenumbers
import json

app = Flask(__name__)


def _url(path):
    return 'http://167.172.156.126:1337' + path


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/test")
def return_files():
    res = requests.get(_url('/users/?mobile=8442590880'))
    data = json.loads(res.text)
    #exist = len(data) > 0
    #name = data[0]['name'] if exist > 0 else 'No user'
    return str(len(data))


@app.route("/sms", methods=['POST'])
def sms_reply():
    #msg = request.form.get('Body')
    trasmisor = request.form.get('From')
    number = trasmisor.split(':')
    parsed_phone = phonenumbers.parse(number[1], None)
    national_phone = phonenumbers.format_number(
        parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL).replace(" ","")
    international_phone = phonenumbers.format_number(
        parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL).replace(" ","")
    get_user = requests.get(_url('/users/?mobile={0}'.format(national_phone)))
    user_json = json.loads(get_user.text)
    print("No1 {0} \nNo2 {1}".format(national_phone,international_phone))
    if len(user_json) <= 0:
        get_user = requests.get(
            _url('/users/?mobile={0}'.format(international_phone)))
        user_json = json.loads(get_user.text)
        if len(user_json) <= 0:
            user_json = False
    if user_json:
        message = ("It's a pleasure talking to you today {0}, how can I help you ?".format(
            user_json[0]['name']))
    else:
        message = (
            "Sorry we did not find your user :C, if you do not have an account you can create one in Heaven Sent")
    # Create reply
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
