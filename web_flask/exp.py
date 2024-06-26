#!/usr/bin/python3

""" Expense Tracker Flask app """

from flask import Flask, jsonify, redirect, request, render_template, url_for
from api import ETapp
from models import storage
from models.category import Category
from models.expense import Expense
from models.user import User, confirm_account, check_string
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(ETapp)
app.static_folder = 'static'
CORS(app)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Returns a JSON if a request route wasn't found """
    return jsonify({'error': 'Not Found'})


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('home.html')


@app.route('/signup', strict_slashes=False)
def signup():
    return render_template("create.html")


@app.route('/signin', strict_slashes=False)
def signin():
    return render_template("signin.html")


@app.route('/dashboard', methods=['GET', 'POST'],
           strict_slashes=False)
def submit_salary():
    if request.method == 'POST':
        salary = request.form.get('salary_amount')
        return render_template('dashboard.html', salary=salary)
    else:
        return render_template('dashboard.html')


@app.route('/submit', methods=['POST', 'GET'],
           strict_slashes=False)
def submit_form():
    """ Handles the case when the user clicks on submit """
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    new = User(**data)
    new.save()
    return render_template('signin.html', success="Account created successfully.. Please signin")


@app.route('/login', methods=['POST', 'GET'],
           strict_slashes=False)
def login():
    """ Confirms a User's details and logs them in to their dashboard """
    email = request.form.get('email')
    password = request.form.get('password')
    user = confirm_account(email, password)
    if user:
        return redirect(url_for('dashboard'))
    return render_template('signin.html', error='Incorrect email or password. Please try again!')


if __name__ == "__main__":
    app.run(debug=True)
