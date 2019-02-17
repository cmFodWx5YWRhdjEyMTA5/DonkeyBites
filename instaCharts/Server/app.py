import os
from flask import Flask,render_template, request,json

app = Flask(__name__)
db_user="abc"
db_password="123"
@app.route('/')
def hello():
    return 'Welcome to Python Flask!'

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    if user == db_user and password == db_password:
        ###  put your code here ###
        #return json.dumps({'status':'OK','user':user,'pass':password});
        return "ok"
    else:
        #return json.dumps({'status':'NOK'});
        return "nok"
if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
