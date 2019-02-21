import sqlite3
from flask import g

def connect_db():
    return sqlite3.connect("database.db")

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

def register_user(name, email, passw):
    try:
        c = get_db()
        result = c.execute("insert into registered_users (name, email, password) values (?,?,?)", [name,email,passw])
        c.commit()
        return True
    except:
        return False

def login_user(email, password, token):
    c = get_db()
    result = c.execute("select * from registered_users where (email) = (?) AND (password) = (?)", [email, password])
    result = result.fetchone()
    if (result is not None):
        #print("hejsan")
        c.execute("insert into logged_in_users (email, token) values (?,?)", [email,token])
        c.commit()
        return True
    else:
        return False

def logout_user(token):
    c = get_db()
    stored_token = get_token()
    if (token == stored_token):
        c.execute("delete from logged_in_users where (token) = (?)", [token])
        c.commit()
        return True
    else:
        return False

def get_token():
    try:
        c = get_db()
        result = c.execute("select token from logged_in_users")
        result = result.fetchone()[0]
        #print(result)
        c.commit()
        return result
    except:
        return False

def delete_user(email):
    try:
        c = get_db()
        result = c.execute("delete from registered_users where (email) = (?)", [email])
        c.commit()
        return True
    except:
        return False

#def user_change_password(token, cur, new):

def user_logged_in(token):
    try:
        c = get_db()
        result = c.execute("select * from logged_in_users where (token) = (?)", [token])
        result = result.fetchone()[0]
        c.commit()
        if (result == None):
            return False
        return True
    except:
        return False

def token_to_email(token):
    try:
        c = get_db()
        result = c.execute("select * from logged_in_users where (token) = (?)", [token])
        result = result.fetchone()[0]
        #print(result)
        c.commit()
        if (result == None):
            return False
        return result
    except:
        return False

def user_exists(email):
    try:
        c = get_db()
        result = c.execute("select * from registered_users where (email) = (?)", [email])
        result = result.fetchone()[0]
        c.commit()
        if (result == None):
            return False
        return True
    except:
        return False

def get_user_data(email):
    try:
        c = get_db()
        result = c.execute("select * from registered_users where (email) = (?)", [email])
        result = result.fetchone()
        c.commit()
        if (result is not None):
            result = {"name" : result[0], "email" : result[1]}
            return result
        result = {}
        return result
    except:
        result = {}
        return result

def get_user_password(email):
    try:
        c = get_db()
        result = c.execute("select * from registered_users where (email) = (?)", [email])
        result = result.fetchone()
        c.commit()
        if (result is not None):
            result = result[2]
            return result
        result = {}
        return result
    except:
        result = {}
        return result

def set_user_password(password, email):
    try:
        c = get_db()
        c.execute("update registered_users set password = (?) where email = (?)", [password, email])
        c.commit()
        return True
    except:
        return False

def get_messages_email(token, email):
    try:
        c = get_db()
        rows = c.execute("select message from messages where (email) = (?)", [email])
        rows = rows.fetchall()
        #result = []
        #for row in range(len(rows)):
        #    print(rows[row][1])
        #return True
        return rows
    except:
        return False

def alter_table(command_string, parameter_array):
    try:
        c = get_db()
        result = c.execute(command_string, parameter_array)
        c.commit()
        return True
    except:
        return False

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        get_db().close()
