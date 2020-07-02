from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    number = request.form.get('From')
    # Create reply
    resp = MessagingResponse()
    resp.message("You said: {0} \n Your number is: {1}".format(msg,number))
    return str(resp)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
