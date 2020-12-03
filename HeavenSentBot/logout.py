from flask import session

def logout():
    session.clear()
    message = "logged out"
    return message