import re

def email(email):
    return re.compile(r'[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z]+\.[0-9a-zA-Z]*\.*[a-zA-Z]+$').match(email)
    
def name(name):
    return not len(name) == 0

def name_with_spaces(name):
    return re.compile(r'\s*[^\s]+\s*$').match(name)

def yes(text):
    return text == "y"

def password(password):
    return not len(password) == 0

