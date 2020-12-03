import json

from flask import Flask, request, session
from . import login
from . import logout

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
        data = json.loads(request.data)
        number = data['number']
        income_msg = data['message']
        user_id = session.get('user_id', 0)
        if user_id != 0:
            if income_msg == 'salir':
                message = logout.logout()
            else:
                message = "aqui va si no es salir"
        else:
            message = login.login(number)
        return message

    return app