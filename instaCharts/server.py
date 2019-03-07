from bottle import route, run, template
import os
import flask

@route('/hello/:name')
def index(name='World'):
    os.system('python3 /home/InstaPy/test.py')
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/pass_val',methods=['POST'])
def pass_val():
    name=requests.args.get('value')
    print('value is ',name)
    return jsonify({'reply':'success'})

run(host='0.0.0.0', port=8089)
