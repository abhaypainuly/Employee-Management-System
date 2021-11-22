from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

# Database Instance
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Creating app instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message("You must be loggeg in to access this page!")
    login_manager.login_view = "auth.login"
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app