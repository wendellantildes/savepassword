from elixir import *

class User(Entity):
    __tablename__ = 'users'

    email = Field(Unicode(50),unique = True,nullable = False)
    name  = Field(Unicode(50),nullable = False)
    password = Field(String(60),nullable = False)
    accounts = OneToMany('Account')
    
    def __repr__(self):
        return '<User "%s" "%s" "%s">' % (self.name,self.email,self.accounts)

class Account(Entity):
    __table__ = 'accounts'

    name        = Field(Binary,unique=True,nullable = False)
    title       = Field(Binary,nullable = False)
    login       = Field(Binary,nullable = True)
    password    = Field(Binary,nullable = False)
    site        = Field(Binary)
    description = Field(Binary, deferred=True)
    user        = ManyToOne('User')
    
    def __repr__(self):
        return '<Account "%s" "%s" "%s" "%s" "%s" "%s">' % (self.name,self.title,self.login,self.password,self.site,self.description)
