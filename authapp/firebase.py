import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth


load_dotenv()


cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
firebase_admin.initialize_app(cred)


db = firestore.client()