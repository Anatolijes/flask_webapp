from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

from src.models import User


class PostFrom(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min=5, max=150)])
    content = StringField('content', validators=[DataRequired(), Length(min=5, max=7000)])
    submit = SubmitField('post!')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('Login')
