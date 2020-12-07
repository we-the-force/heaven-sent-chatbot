import phonenumbers
import contractions
import nltk
from flask import session
from .dictionaries import switch_phrases, help_menu_opciones, es_terms, en_terms, palabras, help_menu_options


def _phone(type_format, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type_format == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


def replace_contractions(text):
    return contractions.fix(text)


def tokenize(text):
    return nltk.word_tokenize(text)


def flow_help():
    session.pop('contacts', None)
    session.pop('memory', None)
    session.pop('thread', None)
    lang = session.get('lang', 'en')
    msg = ("{}".format(palabras[lang].get("help_message")))
    return msg


def flow_menu():
    session.pop('contacts', None)
    session.pop('memory', None)
    session.pop('thread', None)
    msg = ""
    lang = session.get('lang')
    if lang == "es":
        help_menu = help_menu_opciones
    else:
        help_menu = help_menu_options

    for x in help_menu:
        msg += ('- {}\n'.format(x))
    return msg


def change_lang(x):
    session.pop('contacts', None)
    session.pop('memory', None)
    session.pop('thread', None)
    flag_lang = 0
    for element in es_terms:
        if element in x:
            session['lang'] = "es"
            flag_lang = 1
            break

    if not(flag_lang):
        for i in en_terms:
            if i in x:
                session['lang'] = "en"
                flag_lang = 1
                break

    lang = session.get('lang')

    if not(flag_lang):
        msg = "{}".format(palabras[lang].get("not_found_lang"))
    else:
        msg = "{}\n{}".format(palabras[lang].get(
            "lang_changed"), palabras[lang].get("lang"))

    return msg
