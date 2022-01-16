import multitasking
import os
from dotenv import load_dotenv
import hashlib
import time

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



def newAcc(password, apiKey, apiSecret, walletName):

     salt = os.urandom(32)
     key = str(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))
     salt = salt.hex()
     apiKey = encryptKey(apiKey)
     with open('.env', 'r+') as env:
          env.truncate()
          load_dotenv()
          env.write(f'EXISTS=true\nHASH={key}\nSALT={str(salt)}\nKEY={str(apiKey)}\nSECRET={apiSecret}\nWALLETSNUM=1\nWALLETSNAME={walletName}\n') # Encrypt api key
     load_dotenv()
     return True



def newWallet(apiKey, apiSecret, walletName):

     apiKey = encryptKey(apiKey)
     if str(apiKey) not in os.environ.get('KEY'):
          with open('.env', 'r+') as env:
               aEnv = env.read().split('\n')
               aEnv[3] = f'{aEnv[3]}:{apiKey}'
               aEnv[4] = f'{aEnv[4]}:{apiSecret}'
               newWalletNum = str(int(os.environ.get('WALLETSNUM'))+1)
               aEnv[5] = f'WALLETSNUM={newWalletNum}'
               aEnv[6] = f'{aEnv[6]}:{walletName}'
               print(aEnv)
               env.truncate()

          load_dotenv()

          with open('.env', 'r+') as env:
               for line in aEnv:
                    env.write(f'{line}\n')

          load_dotenv()

          return(True)

     else:
          return(False)



#newAcc('coolpassword', 1234, 5678, 'wallet0')
#print(newWallet(5679, 9101, 'wallet1'))