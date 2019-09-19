from .models import Priority, Status
from app import db


def add_standart_values():
    priorities = Priority.query.all()
    status = Status.query.all()
    if not priorities:
        for priority in ['Low', 'Medium', 'High']:
            db.session.add(Priority(priority_title=priority))
    if not status:
        for status in ['In queue', 'In work', 'Done']:
            db.session.add(Status(status_title=status))
    db.session.commit()


def priority_query():
    return Priority.query.all()


def status_query():
    return Status.query.all()