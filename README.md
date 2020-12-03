# heaven-sent-chatbot

## Python 3
python version: 3.6.9
pip version: 

## Flesk
export FLASK_ENV=development
export FLASK_APP=HeavenSentBot
flask run 
## Twilio

## NLTK
### download data
python -m nltk.downloader all

## Instalation
On Ubuntu:
    $ sudo apt-get update
    $ sudo apt-get install python3.8 python3-pip

Create virtual enviroment:
    $ python3 -m venv heaven-bot
    $ source heaven-bot/bin/activate

Install requirements:
    $ pip install requrements.txt

Start server 
    $ python3 app.py

Ngrok
    ./ngrok http 3001

    //get ip from ngrok forwarding

Gunicorn server
    pip install gunicorn
    gunicorn --bind 0.0.0.0:3001 wsgi:app


