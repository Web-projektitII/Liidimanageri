from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime

class Liidi(db.Model):
    __tablename__ = 'liidit'
    # __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(64), unique=True)
    puhelinnumero = db.Column(db.String(15), unique=True)
    sahkoposti = db.Column(db.String(64), unique=True, index=True)
    yksikko = db.Column(db.String(64))
    yhteinen = db.Column(db.String(1))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todennakoisyys = db.Column(db.Numeric(3,2))
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    def __repr__(self):
        return '<Liidi %r>' % self.nimi

class Role(db.Model):
    __tablename__ = 'roles'
    # __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    liidit = db.relationship('Liidi', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email
        }


    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
