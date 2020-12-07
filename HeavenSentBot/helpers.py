import phonenumbers
import contractions
import nltk
from flask import session
from .dictionaries import switch_phrases, help_menu_opciones


def _phone(type_format, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type_format == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


def _return_phrases(arg):
    message = switch_phrases.get(
        arg, "I can't understand you write 'Help' for more information")
    return message


def replace_contractions(text):
    return contractions.fix(text)


def tokenize(text):
    return nltk.word_tokenize(text)


def flow_help():
    session.pop('contacts', None)
    session.pop('memory', None)
    session.pop('thread', None)
    msg = ("Para recibir una mensaje intenta escribiendo algo como: \n\"¿tienes algun mensaje para mi?\" \n\"mandame un mensaje\"\n Si deseas ver las opciones del Bot escribe \"menu\" en un mensaje.")
    return msg

def flow_menu():
    session.pop('contacts', None)
    session.pop('memory', None)
    session.pop('thread', None)
    msg = ""
    for x in help_menu_opciones:
        msg += ('- {}\n'.format(x))
    return msg

