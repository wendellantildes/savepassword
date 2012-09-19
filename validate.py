import re

def email(email):
    return re.compile(r'[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z]+\.[0-9a-zA-Z]*\.*[a-zA-Z]+$').match(email)
    
def name(name):
    return not len(name) == 0

def yes(text):
    if text == "y":
        return True
    else:
        return False

#validacao basica por enquanto
def password(password):
    return not len(password) == 0

# __main__ somente para testes	
if __name__ == "__main__":
    while(True):
        if email(raw_input("Digite um email: ")):
            break 
