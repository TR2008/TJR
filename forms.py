from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])