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
    return unicode(raw_input(message),'utf-8')

class verify_session(object):
    def __init__(self,f):
        self.f = f
        
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            if instance.authenticationService.logged:
                if instance.authenticationService.session_is_expired():
                    instance.authenticationService.logout()
                    instance.authenticationService.logged = False
                    print authentication_expired_session
                    instance.restart_label()
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
        print head
    
    def prompt(self):
        label_now =  "[{date}]{label}".format(date=datetime.now().strftime("%d/%m/%y %H:%M"),label=self.label)
        return raw_input(label_now)
            
    def update_authentication_label(self,email):
        self.label = "{email}{label}".format(email=email,label=">>>")

    def restart_label(self):
        self.label = ">>>"
    
    def type_name(self,message,message_error):
        name = ""
        valid = False
        while(not valid):
            name = self.type_words(message)
            if not validate.name(name):
                print message_error
            else:
                valid = True
        return name

    def type_words(self,message):
        return raw_input_unicode(message)

    def type_word(self,message,message_error):
        name = ""
        valid = False
        while(not valid):
            name = self.type_words(message)
            if not validate.name_with_spaces(name):
                print message_error
            else:
                valid = True
        return name.strip()


    def type_user_email(self,userService,message):
        valid = False
        email = ""
        while(not valid):
            email = raw_input_unicode(message)
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
            password       = unicode(getpass.getpass(password_message),'utf-8')
            password_again = unicode(getpass.getpass(password_message_again),'utf-8')
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
        return unicode(getpass.getpass(prompt_command_login_password),'utf-8')
        
    def print_message(self,message):
        print message

    def print_account(self,key,account):
        print prompt_command_list_accounts_id, account.id
        print prompt_command_list_accounts_name, security.decrypt(key,account.name)
        print prompt_command_list_accounts_title,security.decrypt(key,account.title)
        print prompt_command_list_accounts_login, security.decrypt(key,account.login)
        print prompt_command_list_accounts_password, security.decrypt(key,account.password)
        print prompt_command_list_accounts_site, security.decrypt(key,account.site)
        print prompt_command_list_accounts_description, security.decrypt(key,account.description)		

    def confirm(self,message):
       while True:
           confirm = raw_input_unicode(message)
           if confirm in ["y","n"]:
               return validate.yes(confirm)

class PromptManager(object):
    
    def __init__(self):
        self.prompt = Prompt()
        self.authenticationService = AuthenticationService()
        self.invoker = self.buildInvoker()
        self.options = {}
        self.functions = {}
        self.build_options()
   
    def restart_label(self):
        self.prompt.restart_label()

    def buildInvoker(self):
        invokerMaker = InvokerMaker()
        addUserCommand = AddUserCommand(self.prompt)
        updateUserPasswordCommand = UpdateUserPasswordCommand(self.prompt,self.authenticationService)
        updateUserNameCommand = UpdateUserNameCommand(self.prompt,self.authenticationService)
        updateUserEmailCommand = UpdateUserEmailCommand(self.prompt,self.authenticationService)
        invokerMaker.registerAddUserCommand(addUserCommand).registerUpdateUserPasswordCommand(updateUserPasswordCommand).registerUpdateUserNameCommand(updateUserNameCommand).registerUpdateUserEmailCommand(updateUserEmailCommand)

        loginCommand = LoginCommand(self.prompt,self.authenticationService)
        logoutCommand = LogoutCommand(self.prompt,self.authenticationService)
        exitCommand = ExitCommand(self.prompt,self.authenticationService)
        invokerMaker.registerExitCommand(exitCommand).registerLoginCommand(loginCommand).registerLogoutCommand(logoutCommand)

        addAccountCommand = AddAccountCommand(self.prompt,self.authenticationService)
        deleteAccountCommand = DeleteAccountCommand(self.prompt,self.authenticationService)
        updateAccountCommand = UpdateAccountCommand(self.prompt,self.authenticationService)
        findAccountsCommand = FindAccountsCommand(self.prompt,self.authenticationService)
        listAccountsCommand = ListAccountsCommand(self.prompt,self.authenticationService)
        invokerMaker.registerAddAccountCommand(addAccountCommand).registerDeleteAccountCommand(deleteAccountCommand).registerUpdateAccountCommand(updateAccountCommand).registerFindAccountsCommand(findAccountsCommand).registerListAccountsCommand(listAccountsCommand)

        helpCommand = HelpCommand(self.prompt)
        invokerMaker.registerHelpCommand(helpCommand)
       
        return invokerMaker.buildInvoker()
   
    def build_options(self):
        self.options["add_user"] = re.compile(r'add(\s)user(\s)*$')
        self.functions["add_user"] = self.add_user

        self.options["add_update_user_password"] = re.compile(r'update(\s+)password(\s)*$')
        self.functions["add_update_user_password"] = self.update_user_password
        self.options["add_update_user_name"] = re.compile(r'update(\s+)name(\s)*$')
        self.functions["add_update_user_name"] = self.update_user_name

        self.options["add_update_user_email"] = re.compile(r'update(\s+)email(\s)*$')
        self.functions["add_update_user_email"] = self.update_user_email


        self.options["exit"] = re.compile(r'exit(\s)*$')
        self.functions["exit"] = self.exit
    

        self.options["login"] = re.compile(r'login(\s)*$')
        self.functions["login"] = self.login
            

        self.options["logout"] = re.compile(r'logout(\s)*$')
        self.functions["logout"] = self.logout

        self.options["add_account"] = re.compile(r'add(\s+)account(\s)*$')
        self.functions["add_account"] = self.add_account
            
        self.options["list_accounts"] = re.compile(r'(list)\s+(accounts)\s*$')
        self.functions["list_accounts"] = self.list_accounts
            
        self.options["find_accounts"] = re.compile(r'(find)\s+(accounts)\s*$')
        self.functions["find_accounts"] = self.find_accounts
            
        self.options["delete_account"]  = re.compile(r'delete(\s)+account(\s)*$')
        self.functions["delete_account"] = self.delete_account
            
        self.options["update_account"] = re.compile(r'update(\s)+account(\s)*$')
        self.functions["update_account"] = self.update_account
        
        self.options["help"] = re.compile(r'help(\s)*$')
        self.functions["help"] = self.help_

    
    def add_user(self):
        self.invoker.add_user()

    @login_required
    def update_user_password(self):
        self.invoker.update_user_password()

    @login_required
    def update_user_name(self):
        self.invoker.update_user_name()

    @login_required
    def update_user_email(self):
        self.invoker.update_user_email()

    def login(self):
        self.invoker.login()

    def logout(self):
        self.invoker.logout()

    def exit(self):
        self.invoker.exit()

    @login_required
    def add_account(self):
        self.invoker.add_account()
        
    @login_required
    def delete_account(self):
        self.invoker.delete_account()
        
    @login_required
    def update_account(self):
        self.invoker.update_account()
        
    @login_required
    def find_accounts(self):
        self.invoker.find_accounts()
        
    @login_required
    def list_accounts(self):
        self.invoker.list_accounts()
        
    def help_(self):
        self.invoker.help_()

    def run(self):
        while(True):
            try:
                typed_line = self.prompt.prompt()
                if len(typed_line.strip()) > 0:
                    self.operation(typed_line)
            except KeyboardInterrupt:
                self.prompt.print_message("")

    @verify_session            
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
