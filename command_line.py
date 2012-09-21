#! /usr/bin/python
# -*- coding: utf-8 -*- 

from service import UserService, AuthenticationService, AccountService
from security import Security
from messages import *
import sys
import re
import getpass
from entity import User
import service
import validate
from datetime import datetime
from security import Security
from sqlalchemy.exc import IntegrityError
from argparse import ArgumentParser

security = Security()

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
            if instance.logged:
                return self.f(instance,*args,**kwargs)
            else:
                print prompt_command_login_required
        return wrapper

class Prompt(object):

    def __init__(self):
        self.label = ">>>"
        self.authenticationService = AuthenticationService()
        self.logged = False
        self.command = self.Command()
        self.create_options()		
        print head
        
    def create_options(self):
        self.command.add_exit(self.exit)
        self.command.add_login(self.login)
        self.command.add_logout(self.logout)
        self.command.add_user(self.add_user)
        self.command.add_update_user_password(self.update_user_password)
        self.command.add_update_user_name(self.update_user_name)
        self.command.add_update_user_email(self.update_user_email)
        self.command.add_account(self.add_account)
        self.command.add_list_accounts(self.list_accounts)
        self.command.add_find_account(self.find_account)
        self.command.add_delete_account(self.delete_account)
        self.command.add_update_account(self.update_account)
        self.command.add_help(self.help_command)
    
    def prompt(self):
        while(True):
            try:
                label_now =  "[{date}]{label}".format(date=datetime.now().strftime("%d/%m/%y %H:%M"),label=self.label)
                input = raw_input(label_now)
                if len(input.strip()) > 0:
                    self.operation(input)
            except KeyboardInterrupt:
                print
                continue
    
    @verify_session	
    def operation(self,input):
        try:
            self.command.execute(input)
        except KeyboardInterrupt:
            print
            print prompt_command_operation_aborted		
            
    def exit(self):
        if self.logged:
            print prompt_command_logout
        sys.exit()
        
    def logout(self):
        if self.logged:
            self.authenticationService.logout()
            self.logged = False
            print prompt_command_logout
            self.label = ">>>"

    def add_user(self):
        name = self.type_user_name()
        valid          = False
        userService = UserService()
        email = self.type_user_email(userService)
        #password, password_again = ("","")
        password = self.type_user_password(prompt_command_password,prompt_command_password_again)
        #count = 0
        #valid = False
        #while(not valid):
        #    password       = getpass.getpass(prompt_command_password)
        #    password_again = getpass.getpass(prompt_command_password_again)
        #    if(password != password_again):
        #        count +=1
        #        if(count == 3):
        #            print prompt_command_operation_aborted
        #            return
        #        print prompt_command_password_error
        #    else:
        #       if not validate.password(password):
        #            print prompt_command_password_error_empty
        #        else:
        #            valid = True
        try:
            userService.add(name=name,email=email,password=password)
            print prompt_command_user_added
        except IntegrityError:
            #verificar qual o erro
            print "erro"
    
    def type_user_name(self):
        name = ""
        valid = False
        while(not valid):
            name = raw_input(prompt_command_name)
            if not validate.name(name):
                print prompt_command_name_error
            else:
                valid = True
        return unicode(name,'utf8')

    def type_user_email(self,userService):
        valid = False
        email = ""
        while(not valid):
            email = raw_input(prompt_command_email)
            if not validate.email(email):
                print prompt_command_email_error
            else:
                if(userService.get_user(email) == None):
                    valid = True
                else:
                    print prompt_command_email_duplicated
        return unicode(email,'utf8')

    def type_user_password(self,password_message,password_message_again):
        password, password_again = "",""
        count = 0
        valid = False
        while(not valid):
            password       = getpass.getpass(password_message)
            password_again = getpass.getpass(password_message_again)
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
        return unicode(password,'utf8')

    @login_required
    def add_account(self):
        accountService = AccountService()
        name = ""
        valid = False
        while(not valid):
            name = raw_input(prompt_command_account_name)
            if not validate.name(name):
                print prompt_command_name_error
            else:
                key = self.authenticationService.typed_password 
                if (accountService.get_account(key,name,self.authenticationService.user)==None):
                    valid = True
                else:
                    print prompt_command_account_name_duplicated
        valid = False
        title = ""
        while(not valid):
            title = raw_input(prompt_command_account_title)
            if not validate.name(title):
                print prompt_command_account_title_error
            else:
                valid = True
        valid          = False
        login          = ""
        while(not valid):
            login = raw_input(prompt_command_account_login)
            if not validate.name(login):
                print prompt_command_account_login_error
            else:
                valid = True
        password = ("")
        valid    = False
        while(not valid):
            password       = raw_input(prompt_command_account_password)
            if not validate.name(password):
                print prompt_command_account_password_error
            else:
                valid = True
        site = raw_input(prompt_command_account_site)
        description = raw_input(prompt_command_account_description)
        accountService.add(name,title,login,password,site,description,self.authenticationService.typed_password,self.authenticationService.user)
        print prompt_command_account_added
        
    @login_required
    def update_user_name(self):
        name = self.type_user_name()
        user = self.authenticationService.user 
        userService = UserService()
        userService.update_name(user=user,name=name)
        print prompt_command_update_user_name_updated

    @login_required
    def update_user_password(self):
        new_password = self.type_user_password(password_message=prompt_command_update_user_type_password,password_message_again=messages.prompt_command_update_user_type_password_again)
        user = self.authenticationService.user 
        userService = UserService()
        old_password  = getpass.getpass(prompt_command_login_password)
        if self.authenticationService.password_is_right(old_password):
            userService.update_password(user=user,old_password=old_password,new_password=new_password)
            self.authenticationService.typed_password = new_password
            print prompt_command_update_user_password_updated
        else:
            print authentication_password_error

    @login_required
    def update_user_email(self):
        userService = UserService()
        email = self.type_user_email(userService)
        user = self.authenticationService.user 
        userService.update_email(user=user,email=email)
        self.update_authentication_label(email)
        print prompt_command_update_user_email_updated

    @login_required
    def list_accounts(self,display_quantity=2):
        user = self.authenticationService.user
        userService = UserService()
        accounts = userService.get_accounts(user)
        count = 0
        key = self.authenticationService.typed_password 
        for account in accounts:
            count +=1
            if count > display_quantity:
                count = 0
                print 
                raw_input(prompt_command_more)
            self.print_account(key,account)
            print "#"
    
    @login_required
    def find_account(self,display_quantity=2,**kargs):
        print display_quantity
        accountService = AccountService()
        key = self.authenticationService.typed_password
        found_accounts = None
        if len(kargs)==0:
            word = raw_input(prompt_command_find_accounts_search)
            found_accounts = accountService.find_account(user_password=key,default=word,user=self.authenticationService.user)
        else:
            name  = None
            title = None
            login = None
            site  = None
            description = None
            if "name" in kargs:
                name = kargs["name"]
            if "title" in kargs:
                title = kargs["title"]
            if "login" in kargs:
                login = kargs["login"]
            if "site" in kargs:
                site = kargs["site"]
            if "description" in kargs:
                description = kargs["description"]
            found_accounts = accountsService.find_account(user_password=key,name=name,title=title,login=login,site=site,description=description,user=self.authenticationService.user)
        count = 0
        key = self.authenticationService.typed_password 
        for account in found_accounts:
            count +=1
            print count
            print display_quantity
            if count > display_quantity:
                count = 0
                print 
                raw_input(prompt_command_more)
            self.print_account(key,account)
            print "#"
    
    @login_required
    def delete_account(self):
        name = raw_input(prompt_command_delete_account_name)
        accountService = AccountService()
        key = self.authenticationService.typed_password
        account = accountService.get_account(user_password=key,name=name,user=self.authenticationService.user)
        if account is not None:
            print
            print prompt_command_delete_account_view
            self.print_account(key,account)
            print
            while True:
                confirm = raw_input(prompt_command_delete_account_confirm)
                if confirm in ["y","n"]:
                    if validate.yes(confirm):
                        accountService.delete_account(account)
                        print prompt_command_delete_account_deleted
                    else:
                        print prompt_command_delete_account_not_deleted
                    break
        else:
            print prompt_command_delete_account_not_found
        
    @login_required    
    def update_account(self):
        name = raw_input(prompt_command_update_account)
        accountService = AccountService()
        key = self.authenticationService.typed_password
        account = accountService.get_account(user_password=key,name=name,user=self.authenticationService.user)
        if account is not None:
            print
            print prompt_command_update_account_view
            self.print_account(key,account)
            print
            while True:
                confirm = raw_input(prompt_command_update_account_confirm)
                if confirm in ["y","n"]:
                    if validate.yes(confirm):
                        key = self.authenticationService.typed_password
                        valid = False
                        name = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_name)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.name)
                                    while(not valid):
                                        name = raw_input(prompt_command_account_name)
                                        if not validate.name(name):
                                            print prompt_command_name_error
                                        else:
                                            key = self.authenticationService.typed_password 
                                            if (accountService.get_account(key,name,self.authenticationService.user)==None):
                                                valid = True
                                            else:
                                                print prompt_command_account_name_duplicated
                            break
                        valid = False
                        title = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_title)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.title) 
                                    while(not valid):
                                        title = raw_input(prompt_command_update_account_new_text)
                                        if not validate.name(title):
                                            print prompt_command_account_title_error
                                        else:
                                            valid = True
                                break
                        
                        
                        valid = False
                        login = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_login)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.login) 
                                    while(not valid):
                                        login = raw_input(prompt_command_update_account_new_text)
                                        if not validate.name(login):
                                            print prompt_command_account_title_error
                                        else:
                                            valid = True
                                break

                        valid = False
                        password = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_password)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.password) 
                                    while(not valid):
                                        password = raw_input(prompt_command_update_account_new_text)
                                        if not validate.name(password):
                                            print prompt_command_account_title_error
                                        else:
                                            valid = True
                                break

                        site  = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_site)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.site) 
                                    site = raw_input(prompt_command_update_account_new_text)
                                break

                        description = None
                        while True:
                            confirm = raw_input(prompt_command_update_account_description)
                            if confirm in ["y","n"]:
                                if validate.yes(confirm):
                                    print prompt_command_update_account_original_text,security.decrypt(key,account.description) 
                                    description = raw_input(prompt_command_update_account_new_text)
                                break
                        accountService.update(name=name,title=title,login=login,password=password,site=site,description=description,user_password=key,account=account)
                        print prompt_command_update_account_updated

                    else:
                        print prompt_command_update_account_not_updated
                    break
        else:
            print prompt_command_update_account_not_found


    def print_account(self,key,account):
        print prompt_command_list_accounts_id, account.id
        print prompt_command_list_accounts_name, security.decrypt(key,account.name)
        print prompt_command_list_accounts_title,security.decrypt(key,account.title)
        print prompt_command_list_accounts_login, security.decrypt(key,account.login)
        print prompt_command_list_accounts_password, security.decrypt(key,account.password)
        print prompt_command_list_accounts_site, security.decrypt(key,account.site)
        print prompt_command_list_accounts_description, security.decrypt(key,account.description)		
    
    def login(self):
        security = Security()
        email     = raw_input(prompt_command_login_email )
        password  = getpass.getpass(prompt_command_login_password)
        if self.authenticationService.authenticate(email=email,password=password):
            print authentication_authenticated
            print authentication_welcome.format(name=self.authenticationService.user.name)
            info_session =  self.authenticationService.info_session()
            print authentication_session_begin % info_session[0].strftime("%d/%m/%y %H:%M")
            print authentication_session_end % info_session[1].strftime("%d/%m/%y %H:%M")
            self.logged = True
            self.update_authentication_label(email)
            #self.label = "["+datetime.now().strftime("%d/%m/%y %H:%M")+"]"+email+self.label
        else:
            print self.authenticationService.message_error
            
    def update_authentication_label(self,email):
        self.label = "{email}{label}".format(email=email,label=">>>")

    def help_command(self):
        print prompt_command_help_cancel 
        print prompt_command_help_exit 
        print prompt_command_help_add_user 
        print prompt_command_help_update_name
        print prompt_command_help_update_email
        print prompt_command_help_update_password
        print prompt_command_help_login
        print prompt_command_help_logout
        print prompt_command_help_add_account
        print prompt_command_help_update_account
        print prompt_command_help_delete_account
        print prompt_command_help_list_accounts
        print prompt_command_help_find_account

    class Command(object):
    
        def __init__(self):
            self.commands = {}
            self.functions = {}
            self.special_functions = {}
            
        def add_exit(self,function):
            self.commands["exit"] = re.compile(r'exit(\s)*$')
            self.functions["exit"] = function
            
        def add_user(self,function):
            self.commands["add_user"] = re.compile(r'add(\s)user(\s)*$')
            self.functions["add_user"] = function

        def add_update_user_password(self,function):
            self.commands["add_update_user_password"] = re.compile(r'update(\s)password(\s)*$')
            self.functions["add_update_user_password"] = function

        def add_update_user_name(self,function):
            self.commands["add_update_user_name"] = re.compile(r'update(\s)name(\s)*$')
            self.functions["add_update_user_name"] = function

        def add_update_user_email(self,function):
            self.commands["add_update_user_email"] = re.compile(r'update(\s)email(\s)*$')
            self.functions["add_update_user_email"] = function

        def add_login(self,function):
            self.commands["login"] = re.compile(r'login(\s)*$')
            self.functions["login"] = function
            
        def add_logout(self,function):
            self.commands["logout"] = re.compile(r'logout(\s)*$')
            self.functions["logout"] = function
            
        def add_account(self,function):
            self.commands["add_account"] = re.compile(r'add(\s)account(\s)*$')
            self.functions["add_account"] = function
            
        def add_list_accounts(self,function):
            self.commands["list_accounts"] = re.compile(r'(list)\s(accounts)\s*([0-9]*)\s*$')
            self.functions["list_accounts"] = function
            self.special_functions["list_accounts"] = self.list_accounts
            
        def list_accounts(self,match,input):
            if len(match.group(3)) == 0:
                self.functions["list_accounts"]()
            else:
                self.functions["list_accounts"](int(match.group(3)))
                
        def add_find_account(self,function):
            #self.commands["find_account"] = re.compile(r'(find)\s+(accounts)(?P<arguments>(\s+-[n,t,l,s,d]=[^\s]+)+|\s+)?\s*$')
            self.commands["find_account"] = re.compile(r'(find)\s+(accounts)(?P<arguments>\s*)$')
            self.functions["find_account"] = function
            self.special_functions["find_account"] = self.find_account
        
        def find_account(self,match,input):
            arguments = match.group("arguments")
            self.functions["find_account"](arguments)
            
        def add_delete_account(self,function):
            self.commands["delete_account"]  = re.compile(r'delete(\s)+account(\s)*$')
            self.functions["delete_account"] = function
            
        def add_update_account(self,function):
            self.commands["update_account"] = re.compile(r'update(\s)+account(\s)*$')
            self.functions["update_account"] = function

        def add_help(self,function):
            self.commands["help"] = re.compile(r'help(\s)*$')
            self.functions["help"] = function

            
        def execute(self,input):
            exists = False
            for key in self.commands.keys():
                match = self.commands[key].match(input)
                if match:
                    exists = True
                    if key in self.special_functions.keys():
                        self.special_functions[key](match,input)
                    else:
                        self.functions[key]()
            if not exists:
                print prompt_command_error
                
    
if __name__ == "__main__":
    prompt = Prompt()
    prompt.prompt()
 
    


        
    
    
