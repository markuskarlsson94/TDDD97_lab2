from flask import Flask, request, jsonify
import database_helper
from random import randint

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello hjesna!'


@app.teardown_request
def after_request(exception):
    database_helper.close_db()

@app.route('/register', methods = ['PUT'])
def sign_up():
    print("REGISTRING USER...")
    data = request.get_json()
    name = data['name']
    email = data['email']
    passw = data['password']

    if (len(name) == 0):
        #Too short name, abort!
        response = jsonify({'status' : False, 'message' : 'Too short username'})
    elif (len(email) == 0):
        #Too short email, abort!
        response = jsonify({'status' : False, 'message' : 'Too short email'})
    elif (len(passw) < 8):
        #Too short password, abort!
        response = jsonify({'status' : False, 'message' : 'Too short password'})
    else:
        #Approved data, continue registration
        result = database_helper.add_user(name, email, passw)
        if (result):
            response = jsonify({'status' : True, 'message' : 'User registred!'})
        else:
            response = jsonify({'status' : False, 'message' : 'User already registred!'})
    print("...DONE")
    return response

@app.route('/login', methods = ['PUT'])
def sign_in():
    letters = 'abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    token = ''

    for i in range(36):
        index = randint(0,len(letters)-1)
        token += letters[index]

    print('')
    print(token)

    return '<p>hejsan</p>'

if __name__ == '__main__':
    app.run(debug = True)
