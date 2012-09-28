from prompt import Prompt
from service import *
from messages import *
import sys

class Invoker(object):
    
    def __init__(self,addUserCommand,updateUserPasswordCommand,updateUserNameCommand,updateUserEmailCommand,loginCommand,logoutCommand,exitCommand,addAccountCommand,deleteAccountCommand,updateAccountCommand,findAccountsCommand,listAccountsCommand,helpCommand):
        self.addUserCommand = addUserCommand
        self.updateUserPasswordCommand = updateUserPasswordCommand
        self.updateUserNameCommand = updateUserNameCommand
        self.updateUserEmailCommand = updateUserEmailCommand

        self.loginCommand = loginCommand
        self.logoutCommand = logoutCommand
        self.exitCommand = exitCommand

        self.addAccountCommand = addAccountCommand
        self.deleteAccountCommand = deleteAccountCommand
        self.updateAccountCommand = updateAccountCommand
        self.findAccountsCommand = findAccountsCommand
        self.listAccountsCommand = listAccountsCommand

        self.helpCommand = helpCommand
    
    def add_user(self):
        self.addUserCommand.execute()

    def update_user_password(self):
        self.updateUserPasswordCommand.execute()

    def update_user_name(self):
        self.updateUserNameCommand.execute()

    def update_user_email(self):
        self.updateUserEmailCommand.execute()

    def login(self):
        self.loginCommand.execute()

    def logout(self):
        self.logoutCommand.execute()

    def exit(self):
        self.exitCommand.execute()
        
    def add_account(self):
        self.addAccountCommand.execute()

    def delete_account(self):
        self.deleteAccountCommand.execute()

    def update_account(self):
        self.updateAccountCommand.execute()

    def find_accounts(self):
        self.findAccountsCommand.execute()

    def list_accounts(self):
        self.listAccountsCommand.execute()

    def help_(self):
        self.helpCommand.execute()
        
class InvokerMaker(object):
    
    def __init__(self):
        self.addUserCommand = None
        self.updateUserPasswordCommand = None
        self.updateUserNameCommand = None
        self.updateUserEmailCommand = None
        self.loginCommand = None
        self.logoutCommand = None
        self.exitCommand = None
        self.addAccountCommand = None
        self.deleteAccountCommand = None
        self.updateAccountCommand = None
        self.findAccountsCommand = None
        self.listAccountsCommand = None
        self.helpCommand = None
        
    def registerAddUserCommand(self,command):
        self.addUserCommand = command
        return self

    def registerUpdateUserPasswordCommand(self,command):
        self.updateUserPasswordCommand = command
        return self

    def registerUpdateUserNameCommand(self,command):
        self.updateUserNameCommand = command
        return self

    def registerUpdateUserEmailCommand(self,command):
        self.updateUserEmailCommand = command
        return self

    def registerLoginCommand(self,command):
        self.loginCommand = command
        return self

    def registerLogoutCommand(self,command):
        self.logoutCommand = command
        return self

    def registerExitCommand(self,command):
        self.exitCommand = command
        return self
        
    def registerAddAccountCommand(self,command):
        self.addAccountCommand = command
        return self

    def registerDeleteAccountCommand(self,command):
        self.deleteAccountCommand = command
        return self

    def registerUpdateAccountCommand(self,command):
        self.updateAccountCommand = command
        return self

    def registerFindAccountsCommand(self,command):
        self.findAccountsCommand = command
        return self

    def registerListAccountsCommand(self,command):
        self.listAccountsCommand = command
        return self

    def registerHelpCommand(self,command):
        self.helpCommand = command 
        return self

    def buildInvoker(self):
        return Invoker(self.addUserCommand,self.updateUserPasswordCommand,self.updateUserNameCommand,self.updateUserEmailCommand,self.loginCommand,self.logoutCommand,self.exitCommand,self.addAccountCommand,self.deleteAccountCommand,self.updateAccountCommand,self.findAccountsCommand,self.listAccountsCommand,self.helpCommand)
    
    
class Command(object):

    def __init__(self):
        pass

    def execute(self):
        pass

class AddUserCommand(Command):

    def __init__(self,prompt):
        self.prompt = prompt

    def execute(self):
        self.add_user()


    def add_user(self):
        name = self.prompt.type_name(prompt_command_name,prompt_command_name_error)
        valid          = False
        userService = UserService()
        email = self.prompt.type_user_email(userService,prompt_command_email)
        password = self.prompt.type_user_password(prompt_command_password,prompt_command_password_again)
        try:
            userService.add(name=name,email=email,password=password)
            self.prompt.print_message(prompt_command_user_added)
        except IntegrityError:
            #verificar qual o erro
            self.print_message("erro")

class UpdateUserPasswordCommand(Command):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        self.update_password()

    def update_password(self):
        new_password = self.prompt.type_user_password(password_message=prompt_command_update_user_type_password,password_message_again=messages.prompt_command_update_user_type_password_again)
        user = self.authenticationService.user 
        userService = UserService()
        old_password  = self.prompt.type_password()
        if self.authenticationService.password_is_right(old_password):
            userService.update_password(user=user,old_password=old_password,new_password=new_password)
            self.authenticationService.typed_password = new_password
            self.prompt.print_message(prompt_command_update_user_password_updated)
        else:
            self.prompt.print_message(authentication_password_error)

class UpdateUserEmailCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        userService = UserService()
        email = self.prompt.type_user_email(userService,prompt_command_update_user_type_email)
        user = self.authenticationService.user 
        userService.update_email(user=user,email=email)
        self.prompt.update_authentication_label(email)
        self.prompt.print_message(prompt_command_update_user_email_updated)


class UpdateUserNameCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        name = self.prompt.type_name(prompt_command_name,prompt_command_name_error)
        user = self.authenticationService.user 
        userService = UserService()
        userService.update_name(user=user,name=name)
        self.prompt.print_message(prompt_command_update_user_name_updated)


class ExitCommand(Command):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        if self.authenticationService.logged:
            self.prompt.print_message(prompt_command_logout)
        sys.exit()

class LoginCommand(Command):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        security = Security()
        email     = self.prompt.type_email()
        password  = self.prompt.type_password()
        if self.authenticationService.authenticate(email=email,password=password):
            self.prompt.print_message(authentication_authenticated)
            self.prompt.print_message(authentication_welcome.format(name=self.authenticationService.user.name))
            info_session =  self.authenticationService.info_session()
            self.prompt.print_message(authentication_session_begin % info_session[0].strftime("%d/%m/%y %H:%M"))
            self.prompt.print_message(authentication_session_end % info_session[1].strftime("%d/%m/%y %H:%M"))
            self.prompt.update_authentication_label(email)
        else:
            self.prompt.print_message(self.authenticationService.message_error)

class LogoutCommand(Command):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService
        
    def execute(self):
        if self.authenticationService.logged:
            self.authenticationService.logout()
            self.prompt.print_message(prompt_command_logout)
            self.prompt.update_authentication_label("")

        
 
class AddAccountCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        accountService = AccountService()
        valid = False
        while(not valid):
            name = self.prompt.type_name(prompt_command_account_name,prompt_command_name_error)
            key = self.authenticationService.typed_password 
            if (accountService.get_account(key,name,self.authenticationService.user)==None):
                valid = True    
            else:
                self.prompt.print_message(prompt_command_account_name_duplicated)

        title = self.prompt.type_name(prompt_command_account_title,prompt_command_account_title_error)
        login = self.prompt.type_name(prompt_command_account_login,prompt_command_account_login_error)
        password = self.prompt.type_name(prompt_command_account_password,prompt_command_account_password_error)
        site = self.prompt.type_words(prompt_command_account_site)
        description = self.prompt.type_words(prompt_command_account_description)
        accountService.add(name,title,login,password,site,description,self.authenticationService.typed_password,self.authenticationService.user)
        self.prompt.print_message(prompt_command_account_added)

class DeleteAccountCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        name = self.prompt.type_words(prompt_command_delete_account_name)
        accountService = AccountService()
        key = self.authenticationService.typed_password
        account = accountService.get_account(user_password=key,name=name,user=self.authenticationService.user)
        if account is not None:
            self.prompt.print_message("")
            self.prompt.print_message(prompt_command_delete_account_view)
            self.prompt.print_account(key,account)
            self.prompt.print_message("")
            if self.prompt.confirm(prompt_command_delete_account_confirm):
                accountService.delete_account(account)
                self.prompt.print_message(prompt_command_delete_account_deleted)
            else:
                self.prompt.print_maessage(prompt_command_delete_account_not_deleted)
        else:
            self.prompt.print_message(prompt_command_delete_account_not_found)

class UpdateAccountCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        name = self.prompt.type_words(prompt_command_update_account)
        accountService = AccountService()
        key = self.authenticationService.typed_password
        account = accountService.get_account(user_password=key,name=name,user=self.authenticationService.user)
        if account is not None:
            self.prompt.print_message("")
            self.prompt.print_message(prompt_command_update_account_view)
            self.prompt.print_account(key,account)
            self.prompt.print_message("")
            if self.prompt.confirm(prompt_command_update_account_confirm):
                key = self.authenticationService.typed_password
                name = None
                if self.prompt.confirm(prompt_command_update_account_name):
                    self.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.name))
                    self.prompt.print_message("")
                    while(not valid):
                        name = self.prompt.type_name(prompt_command_account_name,prompt_command_name_error)
                        key = self.authenticationService.typed_password 
                        if (accountService.get_account(key,name,self.authenticationService.user)==None):
                            valid = True    
                        else:
                            self.prompt.print_message(prompt_command_account_name_duplicated)
                title = None
                if self.prompt.confirm(prompt_command_update_account_title):
                    self.prompt.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.title))
                    title = self.prompt.type_name(prompt_command_account_title,prompt_command_account_title_error)
                        
                        
                login = None
                if self.prompt.confirm(prompt_command_update_account_login):
                    self.prompt.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.login)) 
                    login = self.prompt.type_name(prompt_command_account_login,prompt_command_account_login_error)

                password = None
                if self.prompt.confirm(prompt_command_update_account_password):
                    self.prompt.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.password)) 
                    password = self.prompt.type_name(prompt_command_account_password,prompt_command_account_password_error)


                site  = None
                if self.prompt.confirm(prompt_command_update_account_site):
                    self.prompt.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.site)) 
                    site = self.prompt.type_words(prompt_command_update_account_new_text)
                    
                description = None
                if self.prompt.confirm(prompt_command_update_account_description):
                    self.prompt.print_message(prompt_command_update_account_original_text+security.decrypt(key,account.description)) 
                    description = self.prompt.type_words(prompt_command_update_account_new_text)

                accountService.update(name=name,title=title,login=login,password=password,site=site,description=description,user_password=key,account=account)
                self.prompt.print_message(prompt_command_update_account_updated)

            else:
                self.prompt.print_message(prompt_command_update_account_not_updated)
        else:
            self.prompt.print_message(prompt_command_update_account_not_found)

class FindAccountsCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        accountService = AccountService()
        key = self.authenticationService.typed_password
        found_accounts = None
        word = self.prompt.type_words(prompt_command_find_accounts_search)
        found_accounts = accountService.find_account(user_password=key,default=word,user=self.authenticationService.user)
        count = 0
        key = self.authenticationService.typed_password 
        display_quantity = 3
        for account in found_accounts:
            count +=1
            if count > display_quantity:
                count = 0
                self.prompt.print_message("") 
                self.prompt.type_words(prompt_command_more)
            self.prompt.print_account(key,account)
            self.prompt.print_message("#") 

class ListAccountsCommand(object):

    def __init__(self,prompt,authenticationService):
        self.prompt = prompt
        self.authenticationService = authenticationService

    def execute(self):
        user = self.authenticationService.user
        userService = UserService()
        accounts = userService.get_accounts(user)
        count = 0
        key = self.authenticationService.typed_password 
        display_quantity = 3
        if len(accounts) == 0:
            self.prompt.print_message(prompt_command_list_accounts_no_account)  
        else:
            for account in accounts:
                count +=1
                if count > display_quantity:
                    count = 0
                    self.prompt.print_message("")
                    self.prompt.type_words(prompt_command_more)
                self.prompt.print_account(key,account)
                self.prompt.print_message("#")

class HelpCommand(object):

    def __init__(self,prompt):
        self.prompt = prompt

    def execute(self):
        self.prompt.print_message(prompt_command_help_cancel)
        self.prompt.print_message(prompt_command_help_exit)
        self.prompt.print_message(prompt_command_help_add_user)
        self.prompt.print_message(prompt_command_help_update_name)
        self.prompt.print_message(prompt_command_help_update_email)
        self.prompt.print_message(prompt_command_help_update_password)
        self.prompt.print_message(prompt_command_help_login)
        self.prompt.print_message(prompt_command_help_logout)
        self.prompt.print_message(prompt_command_help_add_account)
        self.prompt.print_message(prompt_command_help_update_account)
        self.prompt.print_message(prompt_command_help_delete_account)
        self.prompt.print_message(prompt_command_help_list_accounts)
        self.prompt.print_message(prompt_command_help_find_account)

