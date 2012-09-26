from prompt import Prompt
from service import *
from messages import *
import sys

class Invoker(object):
    
    def __init__(self,addUserCommand,updateUserPasswordCommand,loginCommand,logoutCommand,exitCommand):
        self.addUserCommand = addUserCommand
        self.updateUserPasswordCommand = updateUserPasswordCommand

        self.loginCommand = loginCommand
        self.logoutCommand = logoutCommand
        self.exitCommand = exitCommand
    
    def add_user(self):
        self.addUserCommand.execute()

    def update_user_password(self):
        self.updateUserPasswordCommand.execute()

    def login(self):
        self.loginCommand.execute()

    def logout(self):
        self.logoutCommand.execute()

    def exit(self):
        self.exitCommand.execute()
        
class InvokerMaker(object):
    
    def __init__(self):
        self.addUserCommand = None
        self.updateUserPasswordCommand = None
        self.loginCommand = None
        self.logoutCommand = None
        self.exitCommand = None
        
    def registerAddUserCommand(self,command):
        self.addUserCommand = command
        return self

    def registerUpdateUserPasswordCommand(self,command):
        self.updateUserPasswordCommand = command
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
        
    def buildInvoker(self):
        return Invoker(self.addUserCommand,self.updateUserPasswordCommand,self.loginCommand,self.logoutCommand,self.exitCommand)
    
    
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
        name = self.prompt.type_user_name()
        valid          = False
        userService = UserService()
        email = self.prompt.type_user_email(userService)
        password = self.prompt.type_user_password(prompt_command_password,prompt_command_password_again)
        try:
            userService.add(name=name,email=email,password=password)
            self.prompt.print_message(prompt_command_user_added)
        except IntegrityError:
            #verificar qual o erro
            self.print_message("erro")

class UpdateUserPasswordCommand(Command):

    def __init__(self,prompt,authentication):
        self.prompt = prompt
        self.authentication = authentication

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
            self.prompt_print_message(prompt_command_update_user_password_updated)
        else:
            self.prompt.print_message(authentication_password_error)

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
        
        
