import sqlite3
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../'

DB_FILE = DIR + "data/database.db"

# ==================== Init ====================
def create_tables():
    """Creates tables for users' account info and watchlist."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE user_info (username TEXT, password TEXT, name TEXT)"
    c.execute(command)
    command = "CREATE TABLE money_matters (username TEXT, date DATE, description TEXT, amount MONEY, mode TEXT)"
    c.execute(command)
    db.commit() #save changes
    db.close()  #close database

#create_tables()

# ==================== User Authentication ====================
def add_user(username, password, name):
    """Insert the credentials for newly registered users into the database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO user_info VALUES(?, ?, ?)", (username, password, name))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate user attempting to log in."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for each in c.execute("SELECT user_info.username, user_info.password FROM user_info"):
        if (each[0] == username and each[1] == password):
            db.close()
            return True
    db.close()
    return False

def user_exist(username):
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for each in c.execute("SELECT user_info.username FROM user_info"):
        if (each[0] == username):
            db.close()
            return True
    db.close()
    return False

# ==================== User Information ====================
def get_name(username):
    """Get user's name."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for each in c.execute("SELECT * FROM user_info WHERE username =?", (username,)):
        if (each[0] == username):
            name = each[2]
    db.close()
    return name

def change_name(username, newName):
    """Change user's name."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE user_info SET name =? WHERE username =?", (newName, username))
    db.close()

# ==================== Money Tracker ====================
def get_records(username):
    """Get user's expenses and income records."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    records = []
    for each in c.execute("SELECT * FROM money_matters WHERE username =?", (username,)):
        records.append(each)
    db.close()
    return records

def add_record(username, date, description, amount, mode):
    """Insert the credentials for newly registered users into the database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO money_matters VALUES(?, ?, ?, ?, ?)", (username, date, description, amount, mode))
    db.commit() #save changes
    db.close()  #close database

def remove_record(username, date, description, amount, mode):
    """Insert the credentials for newly registered users into the database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM money_matters WHERE username =? and date =? and description =? and amount =? and mode =?", (username, date, description, amount, mode))
    db.commit() #save changes
    db.close()  #close database
