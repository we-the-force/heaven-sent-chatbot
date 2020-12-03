import phonenumbers
import contractions
import nltk
from .dictionaries import switch_phrases


def _phone(type_format, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type_format == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


def _return_phrases(arg):
    message = switch_phrases.get(arg, "I can't understand you write 'Help' for more information")
    return message

def replace_contractions(text):
    return contractions.fix(text)

def tokenize(text):
    return nltk.word_tokenize(text)

def flow_help():
    return "Sorry, I'm not finished yet."