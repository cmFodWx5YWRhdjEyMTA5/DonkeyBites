import os,requests
from datetime import datetime
from flask import Flask,render_template, request,json
import time
import schedule
from instaPy_functions import *

app = Flask(__name__)
#@app.route('/login')
#def login():
#    os.system('python3 /home/InstaPy/test.py')
#    return 'Welcome to Python Flask!'

@app.route('/start')
def signUp():
    return render_template('start.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    insta_username =  request.form['username'];
    insta_password = request.form['password'];
    users_i_follow = ['avital','avital_cohenlove','avital_akko','jenselter','sivanbaba','amitbetesh']

    schedule.every().day.at("08:00").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("12:45").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("13:16").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("16:30").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("20:00").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("22:19").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("00:15").do(follow(insta_username,insta_password,users_i_follow))
    schedule.every().day.at("04:15").do(follow(insta_username,insta_password,users_i_follow))

    while True:
        schedule.run_pending()
        time.sleep(1)

    return 'ok'

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
