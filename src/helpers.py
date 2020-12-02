from phrases import switch_phrases
import phonenumbers

def _phone(type_format, number):
    parsed_phone = phonenumbers.parse(number, None)
    format_phone = phonenumbers.PhoneNumberFormat.INTERNATIONAL if type_format == 'INT' else phonenumbers.PhoneNumberFormat.NATIONAL
    return phonenumbers.format_number(parsed_phone, format_phone).replace(" ", "")


def _return_phrases(arg):
    message = switch_phrases.get(arg, "I can't understand you write 'Help' for more information")
    return message