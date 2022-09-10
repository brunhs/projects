import os
from os import environ

class Config(object):

    DEBUG = True
    TESTING = True
    FLASK_ENV = 'development'

    basedir = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = environ.get('SECRET_KEY')

    UPLOADS = "/home/username/app/app/static/uploads"

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
