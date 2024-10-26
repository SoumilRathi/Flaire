
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:tJUPNma1TiaoxldI@practices.y36ua.mongodb.net/?retryWrites=true&w=majority&appName=practices"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))



# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
except Exception as e:
    print(e)