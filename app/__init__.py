from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import config

# Database Instance
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Creating app instance
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be loggeg in to access this page!"
    login_manager.login_view = "auth.login"

    migrate.init_app(app, db)
    
    #@app.route('/m')
    #def migrations():
    #    from flask_migrate import migrate as migrates, init
    #    init(directory='migrations', multidb=False)
    #    migrates(directory='migrations', message=None, sql=False, head='head', splice=False, branch_label=None, version_path=None, rev_id=None)
    #    return 'Done!'

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix = '/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app