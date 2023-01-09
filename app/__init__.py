from flask import Flask,jsonify
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# react-liidimanageria varten
from flask_cors import CORS
from config import config
import logging

logging.getLogger('flask_cors').level = logging.DEBUG
bootstrap = Bootstrap()
fa = FontAwesome()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# def kirjautumisvirhe():
#    response = {'virhe':'Kirjautuminen puuttuu.'}
#    return jsonify(response)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
'''Jos blueprintille tarvitaan oma unauthorized_handler, se
voidaan toteuttaa aiheuttamalla puuttuvalla login_view:llä
401-virhe ja käsitellä se blueprintin 401-virhekäsittelijällä.'''
login_manager.blueprint_login_views = {'reactapi':''}
''' Jos yksi login_manager ja sen unauthorized_handler riittävät.
# Tämä ei aiheuta 401-virhettä.
# login_manager.unauthorized_handler(kirjautumisvirhe)'''

def create_app(config_name):
    app = Flask(__name__)
    # react-liidimanageria varten
    CORS(app)
    # app.config["SQLALCHEMY_ECHO"] = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # print(config[config_name].SQLALCHEMY_DATABASE_URI)
    bootstrap.init_app(app)
    fa.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .reactapi import reactapi as reactapi_blueprint
    login_manager.init_app(reactapi_blueprint)
    # Tarvitaanko tätä?
    # CORS(reactapi_blueprint)
    app.register_blueprint(reactapi_blueprint, url_prefix='/reactapi')

    return app
