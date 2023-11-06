import firebase_admin
import pyrebase
from config.firebase_config import firebaseConfig
 

#from dotenv import dotenv_values
#import json
#env = dotenv_values(dotenv_path='.env')

if not firebase_admin._apps :
    cred = firebase_admin.credentials.Certificate("c:/Users/Dell/Downloads/my-api-f9dd3-firebase-adminsdk-j0j8k-97899fa6ce.json")
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

#authentification
authhotel = firebase.auth()