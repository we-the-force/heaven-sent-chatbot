import json

from flask import Flask, request, session
from . import login
from . import logout
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
from .natural_language_processing import normalize
from .dictionaries import exit_terms, help_terms
from .flow_contacts import flow_contact
from .flow_memories import flow_memory
from .helpers import flow_help
from .chat import chatbot


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='beZ}6EmDsU1RNICI!Q)4EWq%?_1/]h',
        DATABASE='https://api.heavensentnow.com',
    )

    # a simple page that says hello
    @app.route('/')
    def _hello():
        return 'Hello'

    # chatbot
    @app.route('/sms', methods=['POST'])
    def _main():
        # get data
        income_msg = request.form.get('Body')
        trasmisor = request.form.get('From')
        number = trasmisor.split(':')[1]
        print(number)
        #data = json.loads(request.data)
        #number = data['number']
        #income_msg = data['message']
        # get session if not exist session equal 0
        user_id = session.get('user_id', 0)

        # if session exist send to NLP
        if user_id != 0:
            # Noise removal
            income_msg = str(normalize(income_msg))
            flag = 0
            for x in exit_terms:
                if x in income_msg:
                    message = logout.logout()
                    flag = 1
                    break

            for x in help_terms:
                if x in income_msg:
                    message = flow_help()
                    flag = 1
                    break

            if not(flag):
                flows = {
                    "contacts": flow_contact,
                    "memories": flow_memory,
                    "phrases": chatbot
                }
                flow = session.get('thread', 'phrases')
                func = flows.get(flow)
                message = func(income_msg)

        # if not send to login
        else:
            message = login.login(number)

        response = MessagingResponse()
        msg = Message()

        if message[0] == 'media':
            msg.media(message[1])
        else:
            msg.body(message)

        response.append(msg)
        # response
        #resp = MessagingResponse()
        # resp.message(message)g
        # return str(resp)
        return str(response)

    return app
