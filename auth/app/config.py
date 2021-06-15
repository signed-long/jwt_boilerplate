from os import environ


class Config(object):
    '''
    '''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    REDIS_URL = environ.get("REDIS_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    '''
    '''
    DEBUG = False


class DevelopmentConfig(Config):
    '''
    '''
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    '''
    '''
    TESTING = True


config_options = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
