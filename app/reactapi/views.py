from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import reactapi
from .. import db
from ..models import User, Liidi
from ..email import send_email
from ..auth.forms import LoginForm, RegistrationForm, LiidiForm
from flask_cors import cross_origin
import sys


@reactapi.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'reactapi' \
            and request.endpoint != 'static':
        return "Unconfirmed user"

@reactapi.route('/poista', methods=['GET', 'POST'])
@login_required
def poista():
    id = request.form.get('id')
    liidi = Liidi.query.get_or_404(id)
    nimi = liidi.nimi
    db.session.delete(liidi)
    db.session.commit()
    # return f"Liidi {nimi} on poistettu."
    response = jsonify(success=True)
    response.status_code = 200
    return response

@reactapi.route('/lista', methods=['GET', 'POST'])
@login_required
def liidit():
    page = request.args.get('page', 1, type=int)
    pagination = Liidi.query.order_by(Liidi.nimi).paginate(
        page, per_page=current_app.config['LM_POSTS_PER_PAGE'],
        error_out=False)
    lista = pagination.items
    # Tämä pitää muuttaa
    # return render_template('auth/liidit.html',lista=lista,pagination=pagination,page=page)
    return

@reactapi.route('/logout')
@login_required
def logout():
    logout_user()
    # Tämä pitää muuttaa
    # flash('You have been logged out.')
    # return redirect(url_for('main.index'))
    return

@reactapi.route('/signin', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def signin():
    # Ajax-versio 
    form = LoginForm()
    sys.stderr.write('\nviews.py,SIGNIN:'+form.email.data+'\n')
    # print('\nviews.py,SIGNUP\n')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # next = request.args.get('next')
            # if next is None or not next.startswith('/'):
            #    next = url_for('main.index')
            sys.stderr.write('\nviews.py,SIGNIN:OK\n')
            return "OK"
        else:
            response = jsonify({'virhe':'Väärät tunnukset'})
            # response.status_code = 200
            return response
            # return "Väärä salasana"    
    else:
        # print("validointivirheet:"+str(form.errors))
        response = jsonify(form.errors)
        # response.status_code = 200
        return response
        # return "Virhe lomakkeessa"
  
@reactapi.route('/signup', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def signup():
    form = RegistrationForm()
    sys.stderr.write('\nviews.py,SIGNUP,email:'+form.email.data+'\n')
    # print('\nviews.py,SIGNUP\n')
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to you by email.')
        return "OK"
    else:
        # print("validointivirheet:"+str(form.errors))
        # return "Virhe lomakkeessa:"+str(form.errors)
        response = jsonify(form.errors)
        response.status_code = 200
        return response

@reactapi.route('/testi', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def testi():
    form = RegistrationForm()
    if form.validate_on_submit():  
        user = User(email=form.email,
                username=form.username,
                password=form.password,
                role_id='',
                confirmed='1')
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            ex_name = ex.__class__.__name__
            if ex_name == 'IntegrityError':
                db.session.rollback()
            return "db:"+ex_name
        return "OK"
    return "Virhe"

