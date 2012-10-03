from hashlib import sha256
from random import randint
import bcrypt
from Crypto.Cipher import AES
from Crypto import Random

class Security:
    def __init__(self):
        self.mode = AES.MODE_CFB
            
    def encrypt(self,key,text):
        iv = Random.new().read(AES.block_size)
        encryptor = AES.new(sha256(key).digest(),self.mode,iv)
        return iv+encryptor.encrypt(text.encode('utf-8'))

    def decrypt(self,key,text):
        decryptor = AES.new(sha256(key).digest(),self.mode, text[:AES.block_size])
        return decryptor.decrypt(text[AES.block_size:])
        
    def password_hash(self,password):
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed
    
    def password_matches(self,password,hashed):
        return  bcrypt.hashpw(password,hashed) == hashed
    
