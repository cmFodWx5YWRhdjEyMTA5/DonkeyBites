import os,requests
from datetime import datetime
from flask import Flask,render_template, request,json

app = Flask(__name__)
db_user="abc"
db_password="123"
@app.route('/login')
def login():
    os.system('python3 /home/InstaPy/test.py')
    return 'Welcome to Python Flask!'

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    follow()
    return 'ok'

def sendTelegram (message):
    requests.get(
        "https://api.telegram.org/bot730982013:AAHjGc7kf3csMAY680TZTn80WFnb-dcdzOs/sendMessage?chat_id=387986068&text=InstaPy {} @ {}".format(message, datetime.now().strftime("%H:%M:%S")))

def follow():
    sendTelegram("WORKING")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
