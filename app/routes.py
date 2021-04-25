from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import login_required
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.models import Expense
from app.forms  import AddExpenseForm
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    expenses = [ 
        {
            'category': 'products',
            'body': '23$'
        },
        {
            'category' : 'clothes',
            'body': '100$'
        },
        {
            'category' : 'beauty products',
            'body': '58$'
        }
    ]
    return render_template('index.html', title = 'Home', expenses = expenses)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect (url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != ' ':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    expenses = user.expense().all()
    if user == current_user:
        return render_template('user.html', user = user, expenses = expenses)
    else:
        raise ValidationError('You have no access to this profile')
    

@app.route('/edit_profile', methods =['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect (url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title = 'Edit Profile', form = form)


@app.route('/add_expense', methods =['GET','POST'])
@login_required
def add_expense():
    form = AddExpenseForm()
    user = User(username=current_user.username)
    username = user.username
    if form.validate_on_submit():
        expense = Expense(category=form.category.data, body=form.body.data, timestamp = form.timestamp.data, user_id = user.id)
        db.session.add(expense)
        db.session.commit()
        flash('You have successfully added new expenses!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.timestamp.data = datetime.now() 
    return render_template('add_expense.html', title = 'Add Expense', form = form)

@app.route('/history')
@login_required
def history():
    user = User(username=current_user.username)
    page = request.args.get('page', 1, type=int)
    expenses = user.expense().paginate(page, app.config['EXPENSES_PER_PAGE'],False)
    next_url = url_for('history', page = expenses.next_num) if expenses.has_next else None
    prev_url = url_for('history', page = expenses.prev_num) if expenses.has_prev else None
    return render_template('history.html', user = user, expenses = expenses.items, next_url = next_url, prev_url = prev_url)

    



