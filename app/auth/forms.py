from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError, SelectField, HiddenField
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import User
# from flask import flash

class LiidiForm(FlaskForm):
    id = HiddenField('id')
    nimi = StringField('Nimi', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-ZÅÄÖa-zåäö][A-ZÅÖÄa-zåäö0-9_. -]*$', 0,
               'Nimessä on vain kirjaimia,välilyöntejä numeroita,pisteitä ja tavu- tai alaviivoja')])
    sahkoposti = StringField('Sähköpostiosoite', validators=[DataRequired(), Length(1, 64),Email()])
    puhelinnumero = StringField('Puhelinnumero', 
        validators=[DataRequired(),Length(5, 15),
        Regexp('^[0-9]*$', 0, 
        'Puhelinnumerossa on vain numeroita')])
    yksikko = SelectField('Yksikkö', choices=[('Business','Business'),('IT','IT'),('HR','HR'),('Muu','Muu')])
    user_id = SelectField(u'Liidimanageri',coerce=int)
    yhteinen = BooleanField('Yhteinen') 
    todennakoisyys = SelectField('Todennäköisyys', choices=[(0.00,'0%'),(0.25,'25%'),(0.50,'50%'),(0.75,'75%'),(1.00,'100%')],coerce=float)
    submit = SubmitField('Lisää tai muuta liidi')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    # flag = False
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            # self.flag = True
            # flash('Username already in use.')
            raise ValidationError('Username already in use.')
