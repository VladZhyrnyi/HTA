from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .appfuncs import priority_query, choose_group, group_members


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


class ChangeGroup(FlaskForm):
    group = QuerySelectField('Choose group', query_factory=choose_group, allow_blank=True)
    submit = SubmitField('Change')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Input text of task..', validators=[DataRequired()])
    executor = QuerySelectField('Executor', query_factory=group_members, allow_blank=False)
    priority = QuerySelectField('Priority', query_factory=priority_query, allow_blank=False)
    submit = SubmitField('Create')