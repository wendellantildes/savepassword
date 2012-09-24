from UserAction import UserAction

class Command(object):

    def __init__(self):
        pass

    def execute(self):
        pass

class CommandAddUser(Command):

    def __init__(self):
        self.user_action = UserAction()

    def execute(self):
        self.user_action.add_user()
