from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from .forms import TaskForm, CreateGroup
from .models import Group, Task, User, Status
from flask_login import current_user, login_required
from datetime import datetime
from app import db

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template("index.html", title='Home')


@main.route('/profile')
@login_required
def profile():
    tasks = Task.query.all()
    return render_template('profile.html', tasks=tasks)


@main.route("/create_task", methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        executor = form.executor.data
        priority = form.priority.data

        new_task = Task(author_id=current_user.id,
                        executor_id=executor,
                        timestamp=datetime.utcnow(),
                        # group=current_user.default_group,
                        priority_id=priority.id,
                        status_id=1,
                        title=title,
                        task_text=text)
        db.session.add(new_task)
        db.session.commit()

        flash('Task successfully created!')
        return redirect(url_for('main.profile'))
    return render_template('create_task.html', title='Create task', form=form)


@main.route("/post/<int:task_id>")
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.title, task=task)


@main.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.task_text = form.text.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('main.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.text.data = task.task_text
    return render_template('create_task.html', title='Update Task',
                           form=form, legend='Update Task')


@main.route("/post/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
        return redirect(url_for('main.profile'))
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.profile'))


@main.route('/crt_grp', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroup()
    if request.method == 'POST':
        if form.validate_on_submit():
            admin = current_user.id
            groupname = form.groupname.data

            group = Group.query.filter_by(groupname=groupname).first()

            if not group:
                new_group = Group(groupname=groupname, group_admin=admin)
                db.session.add(new_group)
                new_group.members.append(User.query.get(current_user.id))
                db.session.commit()
            return redirect(url_for('main.my_groups'))
    return render_template('create_group.html', title='Create group', form=form)


@main.route('/myGroups', methods=['POST', 'GET'])
@login_required
def my_groups():
    grouplist = Group.query.all()
    return render_template('grouplist.html', title='My Groups', list=grouplist)


