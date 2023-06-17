from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class ResetPasswordRequestedForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "email"})
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "new password"})
    repeatedPassword = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "repeat new password"})
    submit = SubmitField('Request Password Reset')