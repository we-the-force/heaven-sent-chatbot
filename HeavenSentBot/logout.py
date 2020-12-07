from flask import session

def logout():
    session.clear()
    message = "Desconectado"
    return message