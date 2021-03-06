import json

from flask import Flask, request, session
from . import login
from . import logout
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
from .natural_language_processing import normalize
from .dictionaries import exit_terms, help_terms, menu_terms, palabras
from .flow_contacts import flow_contact
from .flow_memories import flow_memory
from .helpers import flow_help, flow_menu, change_lang
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
    @app.route('/text', methods=['POST'])
    def _sms():
        # get data
        income_msg = request.values.get('Body', None)
        trasmisor = request.values.get('From')
        # number = trasmisor.split(':')[1]
        print(trasmisor)
        print(income_msg)
        #data = json.loads(request.data)
        #number = data['number']
        #income_msg = data['message']
        # get session if not exist session equal 0
        user_id = session.get('user_id', 0)
        lang = session.get('lang', 'en')
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

            if not(flag):
                if 'menu' in income_msg:
                    message = ("{}\n".format(palabras[lang].get("menu_select")))
                    message += flow_menu()
                    flag = 1

            if not(flag):
                for x in help_terms:
                    if x in income_msg:
                        message = flow_help()
                        flag = 1
                        break

            if not(flag):
                flows = {
                    "contacts": flow_contact,
                    "memories": flow_memory,
                    "language": change_lang,
                    "phrases": chatbot
                }
                flow = session.get('thread', 'phrases')
                func = flows.get(flow)
                message = func(income_msg)

        # if not send to login
        else:
            message = login.login(trasmisor)

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

    # chatbot
    @app.route('/sms', methods=['POST'])
    def _main():
        # get data
        income_msg = request.form.get('Body')
        trasmisor = request.form.get('From')
        
        number = trasmisor.split(':')[1]
        #data = json.loads(request.data)
        #number = data['number']
        #income_msg = data['message']
        # get session if not exist session equal 0
        user_id = session.get('user_id', 0)
        lang = session.get('lang', 'en')
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

            if not(flag):
                if 'menu' in income_msg:
                    message = ("{}\n".format(palabras[lang].get("menu_select")))
                    message += flow_menu()
                    flag = 1

            if not(flag):
                for x in help_terms:
                    if x in income_msg:
                        message = flow_help()
                        flag = 1
                        break

            if not(flag):
                flows = {
                    "contacts": flow_contact,
                    "memories": flow_memory,
                    "language": change_lang,
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
