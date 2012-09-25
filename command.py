from UserAction import UserAction

class Invoker(object):
    
    def __init__(self,addUserCommand):
        self.addUserCommand = addUserCommand
    
    def add_user(self):
        self.addUserCommand.execute()
        
class InvokerMaker(object):
    
    def __init__(self):
        self.addUserCommand = None
        
    def registerAddUserCommand(command)
        self.addUserCommand = command
        
    def buildInvoker(self):
        return Invoker(self.addUserCommand)
    
    
class Command(object):

    def __init__(self):
        pass

    def execute(self):
        pass

class AddUserCommand(Command):

    def __init__(self):
        self.user_action = UserAction()

    def execute(self):
        self.user_action.add_user()
