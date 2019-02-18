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
        print("hejsan")
        c.execute("insert into logged_in_users (email, token) values (?,?)", [email,token])
        c.commit()
        return True
    else:
        return False

def get_token():
    try:
        c = get_db()
        result = c.execute("select token from logged_in_users")
        c.commit()
        return result
    except:
        return False

def delete_user(email):
    try:
        c = get_db()
        #result = c.execute("select * from registered_users where (email) = (?)", [email])
        result = c.execute("delete from registered_users where (email) = (?)", [email])
        #print(result.fetchall())
        c.commit()
        return True
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
