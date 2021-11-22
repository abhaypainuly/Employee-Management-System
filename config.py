# Configuration File
from os import environ, path
from dotenv import load_dotenv

# Load variables from. env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config(object):
    """
        Common Configurations!
    """
    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    # Static Assets
    STATIC_FLODER = "static"
    TEMPLATES_FOLDER = "templates"


class DevelopmentConfig(Config):
    """
        Configurations for Development!
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
        Configurations for Production!
    """
    DEBUG = False


# Mapping enviroment to class
app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Selecting configuration based on environment specfied in .env file
config = app_config[environ.get("FLASK_ENV")] 