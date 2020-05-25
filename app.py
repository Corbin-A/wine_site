from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wine_site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

db = SQLAlchemy(app)
login = LoginManager(app)

from models import User
db.create_all()
from forms import RegisterForm

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data
        user = User(email)
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        flash('Success!')
        return redirect('/')
    
    else:
        return render_template('register.html', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#
#     else:
#        username = request.form.get('username')
 
