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

def raw_input_unicode(message):
    return unicode(raw_input(message),'utf8')

class UserAction(object):

    def add_user(self):
        name = self.type_user_name()
        valid          = False
        userService = UserService()
        email = self.type_user_email(userService)
        password = self.type_user_password(prompt_command_password,prompt_command_password_again)
        try:
            print type(password)
            userService.add(name=name,email=email,password=password)
            print prompt_command_user_added
        except IntegrityError:
            #verificar qual o erro
            print "erro"
    
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
