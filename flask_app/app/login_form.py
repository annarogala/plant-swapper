from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from app import app
from .models import User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "username"})

    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField(validators=[
                           InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=30)], render_kw={"placeholder": "password"})

    submit = SubmitField('Login')
