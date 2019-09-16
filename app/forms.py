from .models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Invalid username')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Invalid username')])
    email = StringField('E-mail', validators=[DataRequired('Invalid email'), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    r_password = PasswordField('Repeat password', validators=[EqualTo('password', message='Passwords not equal')])
    submit = SubmitField('Sign Up')


class CreateGroup(FlaskForm):
    groupname = StringField('Groupname', validators=[DataRequired('Invalid groupname')])
    submit = SubmitField('Create')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Input text of task..', validators=[DataRequired()])
    executor = StringField('Executor')
    priority = SelectField('Priority', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')])
    submit = SubmitField('Create')