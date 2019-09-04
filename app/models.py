from app import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Group(db.Model):

    __tablename__ = "Groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(30), nullable=False)
    group_admin = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __init__(self, groupname, group_admin):
        self.groupname = groupname
        self.group_admin = group_admin


class Task(db.Model):

    __tablename__ = "Tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    executor_id = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    priority = db. Column(db.Integer, nullable=False)
    status = db.Column(db.String(64))
    title = db.Column(db.String(64), nullable=False)
    task_text = db.Column(db.String(140), nullable=False)

    def __init__(self, author_id, executor_id, timestamp, priority, status, title, task_text):
        self.author_id = author_id
        self.executor_id = executor_id
        self.timestamp = timestamp
        self.priority = priority
        self.status = status
        self.title = title
        self.task_text = task_text

    def __repr__(self):
        return f'{str.capitalize(self.title)} : {self.task_text}.'
