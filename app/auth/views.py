from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User, Liidi
from ..email import send_email
from .forms import LoginForm, RegistrationForm, LiidiForm
from flask_cors import cross_origin


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')   
    return render_template('auth/login.html', form=form)


@auth.route('/poista', methods=['GET', 'POST'])
@login_required
def poista():
    id = request.form.get('id')
    liidi = Liidi.query.get_or_404(id)
    db.session.delete(liidi)
    db.session.commit()
    flash(f"Liidi {liidi.nimi} on poistettu.") 
    # flash("Liidi on poistettu.") 
    response = jsonify(success=True)
    response.status_code = 200
    return response

@auth.route('/liidi', methods=['GET', 'POST'])
@login_required
def liidi():
    form = LiidiForm()
    choices = [(c.id, c.username) for c in User.query.order_by('username')]
    form.user_id.choices = choices
    if form.validate_on_submit():
        # liidi = Liidi.query.filter_by(nimi!=form.nimi.data,sahkoposti!=form.sahkoposti.data)
        # result = db.engine.execute("SELECT * FROM liidit")
        # nimet = [row[0] for row in result]
        # print(nimet)
        # Liidi.__table__.insert().prefix_with('IGNORE').values([...])
        """liidi = Liidi(nimi=form.nimi.data,
                    sahkoposti=form.sahkoposti.data,
                    puhelinnumero=form.puhelinnumero.data,
                    yksikko=form.yksikko.data,
                    user_id=int(form.user_id.data),
                    yhteinen=int(not form.yksityinen.data), 
                    todennakoisyys=form.todennakoisyys.data)"""
       
        if form.id.data:
            liidi = Liidi.query.filter_by(id=form.id.data).first()
            try:
                form.populate_obj(liidi)
                db.session.commit()
                flash(f"Liidin {liidi.nimi} tiedot tallennettiin.")  
            except Exception as ex:
                #assert ex.__class__.__name__ == 'IntegrityError'
                ex_name = ex.__class__.__name__
                if ex_name == 'IntegrityError':
                    db.session.rollback()
                    flash("Toinen liidi samoilla tiedoilla on jo olemassa!")  
        else:    
            liidi = Liidi()
            try:
                form.populate_obj(liidi)                
                db.session.add(liidi)
                db.session.commit()
                flash(f"Liidi {liidi.nimi} on lisätty.")  
            # except exc.IntegrityError:
            except Exception as ex:
                #assert ex.__class__.__name__ == 'IntegrityError'
                ex_name = ex.__class__.__name__
                if ex_name == 'IntegrityError':
                    db.session.rollback()
                    flash("Liidi on jo olemassa!") 
                else:
                    flash("Virhe:"+ex_name) 
            finally:
                return redirect(url_for('auth.liidi'))
    # testi = User.query.with_entities(User.id,User.username).order_by('username') 
    # form.user_id.choices = [(c.id, c.username) for c in User.query.order_by('username')]
    if 'id' in request.args:
        id = request.args.get('id')
        liidi = Liidi.query.get_or_404(id)
        form = LiidiForm(obj=liidi)
        form.user_id.choices = choices
    return render_template('auth/liidi.html',form=form)

@auth.route('/liidit', methods=['GET', 'POST'])
@login_required
def liidit():
    page = request.args.get('page', 1, type=int)
    pagination = Liidi.query.order_by(Liidi.nimi).paginate(
        page, per_page=current_app.config['LM_POSTS_PER_PAGE'],
        error_out=False)
    lista = pagination.items
    return render_template('auth/liidit.html',lista=lista,pagination=pagination,page=page)

@auth.route('/tilanne')
@login_required
def tilanne():
    return render_template('auth/tilanne.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit() and form.flag is False:
    if form.validate_on_submit():    
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    # else:
    #  print("flag: "+str(form.flag))

    return render_template('auth/register.html', form=form)

@auth.route('/signin', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return "OK"
    else:
        # print("validointivirheet:"+str(form.errors))
        return "Virhe lomakkeessa"
  
@auth.route('/signup', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def signup():
    form = RegistrationForm()
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
        return "Virhe lomakkeessa"

@auth.route('/testi', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def testi():
    form = RegistrationForm()
    user = User(email=username,
                username=username,
                password=password,
                role_id='',
                confirmed='1'
                )
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as ex:
        ex_name = ex.__class__.__name__
        if ex_name == 'IntegrityError':
            db.session.rollback()
        return "db:"+ex_name
    return "OK"


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
