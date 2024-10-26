import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase app with your service account credentials
cred = credentials.Certificate("google_service_credentials.json")
firebase_admin.initialize_app(cred)

# Access the Firestore database
db = firestore.client()

