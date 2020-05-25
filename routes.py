from flask import redirect, flash, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse

from app import app, db, login

from forms import RegisterForm, LoginForm
from models import User

### Main Site ###

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World!'


### Registration and Login ###

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(form.email.data)
        user.set_password()
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect('/')
    
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.get_user_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Username or Password is Incorrect')
            return redirect(url_for('login'))
        print(user)
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
        
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
