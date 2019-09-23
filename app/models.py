from app import db
from datetime import datetime
from flask_login import UserMixin

members = db.Table('members',
                   db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                   db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
                   )


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(200))
    # task_author = db.relationship('Task', foreign_keys='author', lazy=True)
    # task_executor = db.relationship('Task', foreign_keys='executor', lazy=True)
    default_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    members = db.relationship('Group', secondary=members, backref=db.backref('members', lazy='dynamic'))

    def __repr__(self):
        return self.username


class Group(db.Model):

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(30), nullable=False)
    group_admin = db.Column(db.Integer, db.ForeignKey('users.id'))
    members_id = db.relationship('User', secondary=members, lazy='subquery',
                                 backref=db.backref('groups', lazy=True))
    tasks = db.relationship('Task', backref='for_group')

    def __repr__(self):
        return f'{self.groupname}'


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    group = db.Column(db.Integer, db.ForeignKey('groups.id'))
    priority_id = db. Column(db.Integer, db.ForeignKey('priority.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    title = db.Column(db.String(64), nullable=False)
    task_text = db.Column(db.String(140))
    author = db.relationship('User', foreign_keys=[author_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class Priority(db.Model):

    __tablename__ = 'priority'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    priority_title = db.Column(db.String(15))
    task = db.relationship('Task', backref='priority')

    def __repr__(self):
        return str(self.priority_title)


class Status(db.Model):

    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_title = db.Column(db.String(15))
    task = db.relationship('Task', backref='status')

    def __repr__(self):
        return str(self.status_title)