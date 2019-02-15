# coding=utf-8

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

def create_response(status, message, data = 'N/A'):
    if data == 'N/A':
        return jsonify({'status' : status, 'message' : message})
    else:
        return jsonify({'status' : status, 'message' : message, 'data' : data})

@app.route('/register', methods = ['PUT'])
def sign_up():
    data = request.get_json()
    name = data['name']
    email = data['email']
    passw = data['password']

    if (len(name) == 0):
        response = create_response(False, 'Too short username')
    elif (len(email) == 0):
        response = create_response(False, 'Too short email')
    elif (len(passw) < 8):
        response = create_response(False, 'Too short password')
    else:
        #Approved data, continue registration
        result = database_helper.register_user(name, email, passw)
        if (result):
            response = create_response(True, 'User registred')
        else:
            response = create_response(False, 'User already registred')
    return response

@app.route('/login', methods = ['PUT'])
def sign_in():
    data = request.get_json()
    email = data['email']
    passw = data['password']

    print(email)
    print(passw)

    letters = 'abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    token = ''

    for i in range(36):
        index = randint(0,len(letters)-1)
        token += letters[index]

    #database_helper.login_user(email, token)

    print()
    print(database_helper.get_token())
    
    return create_response(True, 'Successfully signed in', token)

if __name__ == '__main__':
    app.run(debug = True)
