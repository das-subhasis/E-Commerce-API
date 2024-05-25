import os
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv() 

# Loading MongoDB driver
mongo = PyMongo()

# Custom validation function
def validate_api_key(api_key):
    if os.environ.get('API_KEY') == api_key:
        return True
    return False