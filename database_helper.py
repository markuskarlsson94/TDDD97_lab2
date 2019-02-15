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
        result = c.execute("insert into registred_users (name, email, password) values (?,?,?)", [name,email,passw])
        c.commit()
        return True
    except:
        return False

def login_user(email, token):
    try:
        c = get_db()
        result = c.execute("insert into logged_in_users (email, token) values (?,?)", [email,token])
        c.commit()
        return True
    except:
        return False

def get_token():
    try:
        c = get_db()
        result = c.execute("select token from logged_in_users")
        c.commit()
        return result
    except:
        return False

def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        get_db().close()
