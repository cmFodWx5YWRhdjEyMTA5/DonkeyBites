from bottle import route, run, template
from flask import Flask, render_template, redirect, url_for, request

#app = Flask(__name__)

# Route for handling the login page logic
route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

run(host='0.0.0.0', port=8888)
