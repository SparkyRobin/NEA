import multitasking
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()


def encryptKey(apiKey):

     return(apiKey)
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
     salt = bytes.fromhex(salt)
     key = os.environ.get('HASH')

     new_key = str(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))
     print()

     if new_key == key:
          return(True)
     else:
          return(False)

def newAcc(password, apiKey, walletName):

     salt = os.urandom(32)
     key = str(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))
     salt = salt.hex()
     apiKey = encryptKey(apiKey)
     with open('.env', 'r+') as env:
          env.write(f'EXISTS=true\nHASH={key}\nSALT={str(salt)}\nKEY={str(apiKey)}\nWALLETSNUM=1\nWALLETSNAME={walletName}\n') # Encrypt api key
          env.close()

def newWallet(apiKey, walletName):

     apiKey = encryptKey(apiKey)
     with open('.env', 'r+') as env:
          aEnv = env.read().split('\n')
          aEnv[3] = f'{aEnv[3]}:{apiKey}'
          aEnv[4] = str(int(os.environ.get('WALLETSNUM'))+1)
          aEnv[5] = f'{aEnv[5]}:{walletName}'
          env.truncate()
          for line in aEnv:
               env.write(f'{line}\n')

#newAcc('coolpassword', 1234, 'wallet0')
newWallet(5678, 'wallet1')