from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import TaskForm, CreateGroup
from .models import Group, Task
from flask_login import current_user, login_required
from datetime import datetime
from app import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html", title='Home')


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.username, title='User profile')


@main.route("/create_task", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        executor = form.executor.data
        priority = form.priority.data


        task = Task(author_id=current_user.id,
                    executor_id=executor,
                    timestamp=datetime.utcnow(),
                    priority=priority,
                    status=None,
                    title=title,
                    task_text=text)
        db.session.add(task)
        db.session.commit()

        flash('Task successfully created!')
        return redirect(url_for('main.mytask_list'))
    return render_template('create_task.html', title='Create task', form=form)


@main.route('/tsklst', methods=['GET', 'POST'])
@login_required
def mytask_list():
    tasklist = Task.query.all()
    return render_template('tasklist.html', title='Tasklist', list=tasklist)


@main.route('/crt_grp', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroup()
    return render_template('create_group.html', title='Create group', form=form)
