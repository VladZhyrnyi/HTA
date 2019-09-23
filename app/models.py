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
    tasks = db.relationship('Task', backref='author', lazy=True)
    # default_group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    # default_group = db.relationship('Group', foreign_keys=[default_group_id])
    # members = db.relationship('Group', secondary=members, backref=db.backref('members', lazy='dynamic'))


class Group(db.Model):

    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupname = db.Column(db.String(30), nullable=False)
    group_admin = db.Column(db.Integer, db.ForeignKey('users.id'))
    members = db.relationship('User', secondary=members, lazy='subquery',
                              backref=db.backref('groups', lazy=True))
    tasks = db.relationship('Task', backref='for_group')
    # default = db.relationship('User', backref='default_group', lazy=True)

    def __repr__(self):
        return f'{self.groupname}'


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    group = db.Column(db.Integer, db.ForeignKey('groups.id'))
    priority_id = db. Column(db.Integer, db.ForeignKey('priority.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    title = db.Column(db.String(64), nullable=False)
    task_text = db.Column(db.String(140))
    # author = db.relationship('User', backref=db.backref('tasks', lazy=True))
    # executor = db.relationship('User', backref=db.backref('Tasks', lazy=True))
    # group = db.relationship('Group', backref=db.backref('Tasks', lazy=True))


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