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

    #generate token
    letters = 'abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';
    token = ''

    for i in range(36):
        index = randint(0,len(letters)-1)
        token += letters[index]

    #try to login user
    result = database_helper.login_user(email, passw, token)
    if (result):
        return create_response(True, 'Successfully signed in', token)
    else:
        return create_response(False, 'Wrong username or password', token)

    #http://flask.pocoo.org/docs/0.12/patterns/sqlite3/

@app.route('/remove', methods = ['PUT'])
def remove_user():
    data = request.get_json()
    email = data['email']

    result = database_helper.delete_user(email)
    if (result):
        response = create_response(True, 'Successfully removed user')
    else:
        response = create_response(False, 'Failed to remove user')

    return response

@app.route('/logout', methods = ['PUT'])
def logout_user():
    data = request.get_json()
    token = data['token']

    ret = database_helper.logout_user(token)
    if (ret):
        return create_response(True, "User logged out")
    return create_response(False, "Could not log out user")

@app.route('/userloggedin', methods = ['PUT'])
def user_logged_in():
    data = request.get_json()
    token = data['token']
    if database_helper.user_logged_in(token):
        return create_response(True, 'User is logged in')
    #else:
    return create_response(False, 'User is not logged in')

@app.route('/userdatabyemail', methods = ['PUT'])
def get_user_data_by_email():
    data = request.get_json()
    token = data['token']
    email = data['email']

    #print("tokenToEmail: ", database_helper.token_to_email(token))

    if (not database_helper.user_logged_in(token)):
        return create_response(False, 'You are not logged in')
    elif (database_helper.user_exists(email) == False):
        return create_response(False, 'No such user')
    #else:
    result = database_helper.get_user_data(email)
    return create_response(True, "User data retrieved", result)

@app.route('/userdatabytoken', methods = ['PUT'])
def get_user_data_by_token():
    data = request.get_json()
    token = data['token']

    email = database_helper.token_to_email(token)

    if (not database_helper.user_logged_in(token)):
        return create_response(False, 'You are not logged in')
    elif (database_helper.user_exists(email) == False):
        return create_response(False, 'No such user')
    #else:
    result = database_helper.get_user_data(email)
    return create_response(True, "User data retrieved", result)


@app.route('/changepassword', methods = ['PUT'])
def user_change_password():
    data = request.get_json()
    token = data['token']
    old_pass = data['old']
    new_pass = data['new']

    if (not database_helper.user_logged_in(token)):
        return create_response(False, 'You are not logged in')
    elif (len(new_pass) < 8):
        return create_response(False, 'Too short password')
    elif (len(new_pass) > 30):
        return  create_response(False, 'Too long password')

    stored_pass = (database_helper.get_user_password(database_helper.token_to_email(token)))
    if (stored_pass != old_pass):
        return create_response(False, 'Wrong password')
    else:
        email = database_helper.token_to_email(token)
        result = database_helper.set_user_password(new_pass, email)
        if (result):
            return create_response(True, 'Password changed')
    return create_response(False, 'Could not change password')

@app.route('/messagesbyemail', methods = ['PUT'])
def user_get_messages():
    data = request.get_json()
    token = data['token']
    email = data['email']

    print(database_helper.get_messages_email(token, email))
    return "ssees"


if __name__ == '__main__':
    app.run(debug = True)
