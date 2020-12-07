from flask import session
from .flow_contacts import flow_contact
from .dictionaries import memories_messages, language_terms, switch_phrases


def chatbot(x):
    flag = 0
    for y in memories_messages:
        if y in x:
            session['thread'] = 'contacts'
            msg = flow_contact()
            flag = 1
            break

    if not(flag):
        for y in language_terms:
            if y in x:
                #session['thread'] = 'language'
                msg = ("cambiar idioma {}".format(x))
                flag = 1
                break
    
    if not(flag):
        for i in switch_phrases.keys():
            if i in x:
                msg = switch_phrases.get(i)
                flag = 1

    if not(flag):
        msg = "Lo siento no pude entenderte. Escribe 'Ayuda' para obtener más información.\n "
    return msg
