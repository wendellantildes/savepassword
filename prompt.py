#! /usr/bin/python
# -*- coding: utf-8 -*- 
from command import *
from messages import *
import getpass
import validate
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import re

def raw_input_unicode(message):
    return unicode(raw_input(message),'utf8')

class verify_session(object):
    def __init__(self,f):
        self.f = f
        
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            if instance.logged:
                if instance.authenticationService.session_is_expired():
                    instance.authenticationService.logout()
                    instance.logged = False
                    print authentication_expired_session
                    instance.label = ">>>"
            return self.f(instance,*args,**kwargs)
        return wrapper

class login_required(object):
    def __init__(self,f):
        self.f = f
        
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            if instance.authenticationService.logged:
                return self.f(instance,*args,**kwargs)
            else:
                print prompt_command_login_required
        return wrapper
        
class Prompt(object):
    def __init__(self):
        self.label = ">>>"
        #self.create_options()       
        print head
    
    def prompt(self):
        label_now =  "[{date}]{label}".format(date=datetime.now().strftime("%d/%m/%y %H:%M"),label=self.label)
        return raw_input(label_now)
            
    def update_authentication_label(self,email):
        self.label = "{email}{label}".format(email=email,label=">>>")
    
    def type_user_name(self):
        name = ""
        valid = False
        while(not valid):
            name = raw_input_unicode(prompt_command_name)
            if not validate.name(name):
                print prompt_command_name_error
            else:
                valid = True
        return name

    def type_user_email(self,userService):
        valid = False
        email = ""
        while(not valid):
            email = raw_input_unicode(prompt_command_email)
            if not validate.email(email):
                print prompt_command_email_error
            else:
                if(userService.get_user(email) == None):
                    valid = True
                else:
                    print prompt_command_email_duplicated
        return email

    def type_user_password(self,password_message,password_message_again):
        password, password_again = "",""
        count = 0
        valid = False
        while(not valid):
            password       = unicode(getpass.getpass(password_message),'utf8')
            password_again = unicode(getpass.getpass(password_message_again),'utf8')
            if(password != password_again):
                count +=1
                if(count == 3):
                    print prompt_command_operation_aborted
                    return
                print prompt_command_password_error
            else:
                if not validate.password(password):
                    print prompt_command_password_error_empty
                else:
                    valid = True
        return password
    
    def type_email(self):
        return raw_input_unicode(prompt_command_login_email)

    def type_password(self):
        return getpass.getpass(prompt_command_login_password)
        

    def print_message(self,message):
        print message

class PromptManager(object):
    
    def __init__(self):
        self.prompt = Prompt()
        self.authenticationService = AuthenticationService()
        self.logged = False
        self.invoker = self.buildInvoker()
        self.options = {}
        self.functions = {}
        self.build_options()
    
    def buildInvoker(self):
        invokerMaker = InvokerMaker()
        addUserCommand = AddUserCommand(self.prompt)
        updateUserPasswordCommand = UpdateUserPasswordCommand(self.prompt,self.authenticationService)
        invokerMaker.registerAddUserCommand(addUserCommand).registerUpdateUserPasswordCommand(updateUserPasswordCommand)

        loginCommand = LoginCommand(self.prompt,self.authenticationService)
        logoutCommand = LogoutCommand(self.prompt,self.authenticationService)
        exitCommand = ExitCommand(self.prompt,self.authenticationService)
        invokerMaker.registerExitCommand(exitCommand).registerLoginCommand(loginCommand).registerLogoutCommand(logoutCommand)
       
        return invokerMaker.buildInvoker()
    
    def build_options(self):
        self.options["add_user"] = re.compile(r'add(\s)user(\s)*$')
        self.functions["add_user"] = self.add_user

        self.options["add_update_user_password"] = re.compile(r'update(\s)password(\s)*$')
        self.functions["add_update_user_password"] = self.update_user_password

        self.options["exit"] = re.compile(r'exit(\s)*$')
        self.functions["exit"] = self.exit
    

        self.options["login"] = re.compile(r'login(\s)*$')
        self.functions["login"] = self.login
            

        self.options["logout"] = re.compile(r'logout(\s)*$')
        self.functions["logout"] = self.logout

        
    
    def add_user(self):
        self.invoker.add_user()

    @login_required
    def update_user_password(self):
        self.invoker.update_user_password()

    def login(self):
        self.invoker.login()

    def logout(self):
        self.invoker.logout()
        print self.authenticationService.logged

    def exit(self):
        self.invoker.exit()
        
    def run(self):
        while(True):
            try:
                typed_line = self.prompt.prompt()
                if len(typed_line.strip()) > 0:
                    self.operation(typed_line)
            except KeyboardInterrupt:
                self.prompt.print_message("")

                
    def operation(self,typed_line):
        exists = False
        for key in self.options.keys():
            match = self.options[key].match(typed_line)
            if match:
                self.functions[key]()
                exists = True
        if not exists:
            self.prompt.print_message(prompt_command_error)


if __name__ == "__main__":
    prompt_manager = PromptManager()
    prompt_manager.run()
