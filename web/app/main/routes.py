from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_user
from app.models import User
from flask_login import login_required
#from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.main.forms import EditProfileForm
from app.models import Expense
from app.main.forms  import AddExpenseForm
from datetime import datetime
from app.main import bp
from app.main.analyse import analyse,exponential_smoothing


@bp.route('/')
@bp.route('/index')
@login_required
def index():
<<<<<<< HEAD
<<<<<<< HEAD
    """ Function to access home page"""
=======
    """Function provides to home page"""
>>>>>>> dev1
=======
    """Function provides to home page"""
>>>>>>> dev1
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

@bp.route('/user/<username>')
@login_required
def user(username):
<<<<<<< HEAD
<<<<<<< HEAD
    """ Function to access home page"""
=======
    """ Function allows to access profile page """
>>>>>>> dev1
=======
    """ Function allows to access profile page """
>>>>>>> dev1
    user = User.query.filter_by(username = username).first_or_404()
    expenses = Expense.query.filter_by(user_id = user.id)
    #expenses = user.expense().all()
    if user == current_user:
        return render_template('user.html', user = user, expenses = expenses)
    else:
        raise ValidationError('You have no access to this profile')
    

@bp.route('/edit_profile', methods =['GET','POST'])
@login_required
def edit_profile():
    """ Function to access edit profile page """
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect (url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title = 'Edit Profile', form = form)


@bp.route('/add_expense', methods =['GET','POST'])
@login_required
def add_expense():
    """ Function to add expense page """
    form = AddExpenseForm()
    #user = User(username=current_user.username)
    #username = user.username
    if form.validate_on_submit():
        expense = Expense(category=form.category.data, body=form.body.data, timestamp = form.timestamp.data, user_id = current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('You have successfully added new expenses!')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.timestamp.data = datetime.now() 
    return render_template('add_expense.html', title = 'Add Expense', form = form)

@bp.route('/history')
@login_required
def history():
    """ Function to access history page """
    user = User(username=current_user.username)
    page = request.args.get('page', 1, type=int)
    expenses = Expense.query.filter_by(user_id = current_user.id)
    #expenses = expenses.paginate(page, app.config["EXPENSES_PER_PAGE"], False)
    expenses = expenses.order_by(Expense.timestamp.desc())
    #expense_first = expenses[-1]
    #expense_last = expenses[0]
    #first_time = expense_first.timestamp
    #print(type(first_time))  #class datetime.datetime
    #first_time_year = first_time.year
    #first_time_month = first_time.month
    #first_time = "first_time_month"+'-'+"first_time_year"
    #print(first_time)
    #last_time = expense_last.timestamp
    #last_time_year = last_time.year
    #last_time_month = last_time.month
    #a = {}
    #t = 0
    #first_expense=expenses[0]
    #a[first_expense.export_date()]=int(first_expense.body)
    #for expense in expenses: 
    #    d = expense.export_date()
    #    if d==first_expense.export_date():
    #        t+=int(expense.body)
    #        a[expense.export_date()] = t
    #    else:
    #        t = int(expense.body)
    #        a[expense.export_date()] = t
    #        first_expense=expense
    #print(a)
    expenses = expenses.paginate(page, current_app.config["EXPENSES_PER_PAGE"], False)
    next_url = url_for('main.history', page = expenses.next_num) if expenses.has_next else None
    prev_url = url_for('main.history', page = expenses.prev_num) if expenses.has_prev else None
    return render_template('history.html', user = user, expenses = expenses.items, next_url = next_url, prev_url = prev_url)


@bp.route('/analysis')
@login_required
def analysis():
    """ Function to access analyse page """
    user=User(username=current_user.username)
    expenses = Expense.query.filter_by(user_id = current_user.id)
    expenses = expenses.order_by(Expense.timestamp.desc())
    a = {}
    t = 0
    if expenses[0]:
        first_expense=expenses[0]
        a[first_expense.export_date()]=int(first_expense.body)
        for expense in expenses:
            d = expense.export_date()
            if d==first_expense.export_date():
                t+=int(expense.body)
                a[expense.export_date()] = t
            else:
                t = int(expense.body)
                a[expense.export_date()] = t
                first_expense=expense
        total_amount = analyse(a,exponential_smoothing)
    else:
        total_amount = 0
    return render_template('analysis.html', user=user, total_amount=total_amount )
#    print(a)
#    expense_first = expenses[-1]
#    expense_last = expenses[0]
#    first_time = expense_first.timestamp
#    last_time = expense_last.timestamp
#    timestamps = [expenses.timestamp.all()]
#    print(timestamps)
#    analyse(data)
#    return render_template('analysis.html', user=user)
