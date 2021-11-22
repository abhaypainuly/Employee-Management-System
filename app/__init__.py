from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

# Database Instance
db = SQLAlchemy()

def create_app():
    # Creating app instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
        
    return app