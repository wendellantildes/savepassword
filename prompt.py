
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
            if instance.logged:
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
        try:
            label_now =  "[{date}]{label}".format(date=datetime.now().strftime("%d/%m/%y %H:%M"),label=self.label)
            return raw_input(label_now)
        except KeyboardInterrupt:
            print

class PromptManager(object):
    
    def __init__(self):
        self.prompt = Prompt()
        self.authenticationService = AuthenticationService()
        self.logged = False
        self.command = self.Command()
    
    def run(self):
        while(True):
            typed_line = self.prompt()
            if len(input.strip()) > 0:
                self.operation(typed_line)     
