from app import db
from datetime import datetime
from flask_login import UserMixin

members = db.Table('members',
                   db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
                   db.Column('group_id', db.Integer, db.ForeignKey('Groups.id'))
                   )


class User(db.Model, UserMixin):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(200))
    members = db.relationship('Group', secondary=members, backref=db.backref('members', lazy='dynamic'))


class Group(db.Model):

    __tablename__ = "Groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(30), nullable=False)
    group_admin = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return f'{self.groupname}'


class Task(db.Model):

    __tablename__ = "Tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    executor_id = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    for_group = db.Column(db.Integer, db.ForeignKey('Groups.id'))
    priority = db. Column(db.Integer, nullable=False)
    status = db.Column(db.String(64))
    title = db.Column(db.String(64), nullable=False)
    task_text = db.Column(db.String(140), nullable=False)
    author = db.relationship('User', backref=db.backref('Tasks', lazy=True))
    group = db.relationship('Group', backref=db.backref('Tasks', lazy=True))
