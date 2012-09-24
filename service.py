#! /usr/bin/python
# -*- coding: utf-8 -*- 

from elixir import *
from security import Security
import messages
import gettext 
import locale
from entity import User
from entity import Account
import service
from datetime import datetime,timedelta

security = Security()
metadata.bind = 'sqlite:///accounts.sqlite'
metadata.bind.encoding = 'utf8'
metadata.bind.echo = False
setup_all()
create_all()
commit = session.commit

class UserService:
    
    def add(self,name,email,password):
        user = User(name=name,email=email.encode("utf-8"),password=security.password_hash(password).encode("utf-8"))
        commit()
            
    def get_user(self,email):
        return User.query.filter(User.email==email).first()
        
    def get_accounts(self,user):
        return user.accounts

    def update_password(self,user,old_password,new_password):
        accounts = user.accounts
        for account in accounts:
            name = security.decrypt(old_password,account.name)
            account.name = security.encrypt(new_password,name)

            title = security.decrypt(old_password,account.title)
            account.title = security.encrypt(new_password,title)

            login = security.decrypt(old_password,account.login)
            account.login = security.encrypt(new_password,login)

            password = security.decrypt(old_password,account.password)
            account.password = security.encrypt(new_password,password)

            site = security.decrypt(old_password,account.site)
            account.site = security.encrypt(new_password,site)

            description = security.decrypt(old_password,account.description)
            account.description = security.encrypt(new_password,description)
        user.password = security.password_hash(new_password)
        commit()
    
    def update_login(self,user,email):
        user.email = email
        commit()

    def update_name(self,user,name):
        user.name = name
        commit()

class AccountService:
    
    def add(self,name,title,login,password,site,description,user_password,user):
        name        = security.encrypt(user_password,name)
        title       = security.encrypt(user_password,title)
        login       = security.encrypt(user_password,login)
        password    = security.encrypt(user_password,password)
        site        = security.encrypt(user_password,site)
        description = security.encrypt(user_password,description)
        account     = Account(name=name,title=title,login=login,password=password,site=site,description=description,user=user)
        commit()
        
    def get_account(self,user_password,name,user):
        accounts = user.accounts
        for account in accounts:
            if security.decrypt(user_password,account.name) == name:
                return account
        return None
        
    def find_account(self,user_password,default,user):
        accounts = user.accounts
        found_accounts = []
        default = default.lower()
        for account in accounts:
            if (security.decrypt(user_password,account.name).lower().find(default) != -1):
                found_accounts.append(account)
                continue
            if (security.decrypt(user_password,account.title).lower().find(default) != -1):
                found_accounts.append(account)
                continue
            if (security.decrypt(user_password,account.login).lower().find(default) != -1):
                found_accounts.append(account)
                continue
            if (security.decrypt(user_password,account.site).lower().find(default) != -1):
                found_accounts.append(account)
                continue
            if (security.decrypt(user_password,account.description).lower().find(default) != -1):
                found_accounts.append(account)
                continue
        return found_accounts
    
    def find_account_custom(self,user_password,name,title,login,site,description,user):
        accounts = user.accounts
        found_accounts = []
        for account in accounts:
            if (name is not None and security.decrypt(user_password,account.name).lower().find(name.lower()) != -1):
                found_accounts.append(account)
                continue
            if (title is not None and security.decrypt(user_password,account.title).lower().find(title.lower()) != -1):
                found_accounts.append(account)
                continue
            if (login is not None and security.decrypt(user_password,account.login).lower().find(login.lower()) != -1):
                found_accounts.append(account)
                continue
            if (site is not None and security.decrypt(user_password,account.site).lower().find(site.lower()) != -1):
                found_accounts.append(account)
                continue
            if (description is not None and security.decrypt(user_password,account.description).lower().find(description.lower()) != -1):
                found_accounts.append(account)
                continue
        return found_accounts
    
    
    def find_account_name(self,user_password,name,user):
        pass

    def find_account_title(self):
        pass
        
    def find_account_login(self):
        pass
        
    def find_account_site(self):
        pass
        
    def find_account_description(self):
        pass

    def delete_account(self,account):
        account.delete()
        commit()

    def update(self,name,title,login,password,site,description,user_password,account):
        if name is not None:
            account.name = security.encrypt(user_password,name)
        if title is not None:
            account.title = security.encrypt(user_password,title)
        if login is not None:
            account.login = security.encrypt(user_password,login)
        if password is not None:
            account.password = security.encrypt(user_password,password)
        if site is not None:
            account.site = security.encrypt(user_password,site)
        if description is not None:
            account.description - security.encrypt(user_password,description)
        commit()

        
class AuthenticationService:
    
    def __init__(self):
        self.user = None
        self.message_error = None
        self.time_login    = None
        self.logged        = False
        self.typed_password =  None
        self.time_session = 3
    
    #TODO: verificar esse password guardado aqui	
    def authenticate(self,email,password):
        userService = UserService()
        self.user = userService.get_user(email)
        if self.user is None:
            self.message_error = messages.authentication_email_error
            return False
        if security.password_matches(password,self.user.password):
            self.time_login = datetime.now()
            self.logged     = True
            self.typed_password =  password
            return True
        else:
            self.message_error = messages.authentication_password_error
            return False
            
    def get_login(self):
        return self.user.login

    def password_is_right(self,password):
        return security.password_matches(password,self.user.password) 
        
    def logout(self):
        self = AuthenticationService()
    
    def session_is_expired(self):
        if datetime.now()-timedelta(minutes=self.time_session) >= self.time_login:
            return True
        else:
            return False
            
    def info_session(self):
        begin = self.time_login
        end   = self.time_login + timedelta(minutes=self.time_session)
        return (begin,end)
        
        
    
        
