from flask import Flask
from .config import Config  
from .extensions import mongo  
from .routes import api  

def create_app():
    # Create a Flask app instance
    app = Flask(__name__) 
    
    # Load configuration settings from the Config class
    app.config.from_object(Config)  
    
    # Initialize MongoDB connection
    mongo.init_app(app)  
    
    # Register API routes
    app.register_blueprint(api)  
    
    return app  
