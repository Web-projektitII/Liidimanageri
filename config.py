import os
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <liidimanageri@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = os.environ.get('ENV')
    if ENV == 'prod':
        DB_URL = 'us-cdbr-east-05.cleardb.net'
        DB_NAME = 'heroku_3362c192f18dd93'
        DB_USERNAME = os.environ.get('DB_USERNAME_TUOTANTO')
        DB_PASSWORD = os.environ.get('DB_PASSWORD_TUOTANTO')
        DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
    else:
        DB_URL = 'localhost'
        DB_NAME = 'liidimanageri'
        DB_USERNAME = 'root'
        DB_PASSWORD = ''
        DB_URL = 'localhost'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class LiidimanageriConfig(Config):
    DB_URL = Config.DB_URL
    DB_NAME = Config.DB_NAME
    DB_USERNAME = Config.DB_USERNAME
    DB_PASSWORD = Config.DB_PASSWORD
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@'+DB_URL+':3306/' + DB_NAME
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_ECHO = "debug"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Liidimanageri]'
    FLASKY_MAIL_SENDER = 'Liidimanageri Admin <omniakurssi@gmail.com>'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'liidimanageri' : LiidimanageriConfig,
    'default': LiidimanageriConfig

    # 'default': DevelopmentConfig
}
