from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from models import User

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.get_user_by_email(email.data)
        if user:
            raise ValidationError('This email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

#     def validate_password(self, email, password):
#         print('validating email and password')
#         print(f'email: {email.data}')
#         user = User.get_user_by_email(email.data)
#         print(user)
# 
#         if user is None or not user.check_password(password.data):
#             raise ValidationError('Username or Password was Incorrect.')
