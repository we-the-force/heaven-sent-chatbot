from flask import session
from .flow_contacts import flow_contact
from .dictionaries import memories_messages, language_terms, switch_phrases, palabras, languages


def chatbot(x):
    flag = 0
    lang = session.get('lang', "en")
    for y in memories_messages:
        if y in x:
            session['thread'] = 'contacts'
            msg = flow_contact()
            flag = 1
            break

    if not(flag):
        for y in language_terms:
            if y in x:
                session['thread'] = 'language'
                msg = ("{}\n".format(palabras[lang].get("change_lang")))
                for i in languages.get(lang):
                    msg += ("- {}\n".format(i))
                flag = 1
                break

    if not(flag):
        for i in switch_phrases.keys():
            if i in x:
                msg = switch_phrases.get(i)
                flag = 1

    if not(flag):
        msg = ("{}\n".format(palabras[lang].get("can_not_understand")))
    return msg
