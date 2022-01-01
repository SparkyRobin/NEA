import multitasking
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def initCheck():

     hasAcc = os.environ.get('EXISTS')
     if hasAcc == 'true':
          return(True)
     else:
          return(False)

def passCheck(password):

     user = os.environ.get('USER')
     salt = os.environ.get('SALT')
     print(salt)
     salt = salt.encode('latin1')
     key = os.environ.get('HASH')

     new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)


     if new_key == key:
          print('Password is correct')
     else:
          print('Password is incorrect')

def newAcc(password, apiKey):

     salt = os.urandom(32)
     key = str(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))
     salt = salt.decode('latin1')
     print(salt)
     with open('.env', 'r+') as env:
          env.write(f'EXISTS=true\nHASH={key}\nSALT={str(salt)}\nKEY={str(apiKey)}') # Encrypt api key

newAcc("coolpassword", 1234)
passCheck("coolpassword")