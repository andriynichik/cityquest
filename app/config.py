import os

class Config(object):

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/geodata'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True