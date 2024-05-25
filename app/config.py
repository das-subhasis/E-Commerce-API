import os
from dotenv import load_dotenv
load_dotenv()  

class Config:
    # Import secret key from .env file
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    # Extract mongo uri from .env file
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ecommerce')
