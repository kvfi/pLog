from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from plog import app
from plog.forms import LoginForm
from plog.models import User


@app.errorhandler(403)
def internal_error():
    return render_template('errors/403.html'), 403


@app.route('/')
@app.route('/index', endpoint='dashboard')
@login_required
def index():
    meta = {'title': 'Index'}
    return render_template('index.html', meta=meta)


@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    meta = {'title': 'Log In'}
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            print(check_user)
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('dashboard'))
    return render_template('login.html', meta=meta, form=form)


@app.route('/logout')
def logout():
    u = logout_user()
    if u:
        flash('You were successfully logged in')
    return redirect(url_for('login'))


@app.route('/todos')
def todos():
    meta = {'title': 'Tasks'}
    return render_template('todos.html', todos='x', meta=meta)


@app.route('/user')
@login_required
def user():
    return generate_password_hash('k0ù@£!4030')
    '''user = User('ouafi@ouafi.net', 'k0ù@£!4030')
    if user.find_by_email():
        return 'yes'
    else:
        return 'no user'''

@app.route('/token')
@login_required
def token():
    return 'xd'

