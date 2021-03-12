from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Daria'}
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
    return render_template('index.html', title = 'Home',  user = user, expenses = expenses)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Sign in', form=form)
