import os

from flask import Flask, render_template, request, flash, session, url_for, redirect

from util import db

app = Flask(__name__)

app.secret_key=os.urandom(32)

# allows user to log into their account
@app.route("/")
def login():
    return render_template("login.html", title = "Login", heading = "Login")

# allows user to register a new account
@app.route("/register")
def register():
    return render_template("register.html", title = "Register", heading = "Register")

# authorizes user
@app.route("/auth", methods = ["GET", "POST"])
def auth():
    given_user = request.form["username"]
    given_pwd = request.form["password"]
    if db.auth_user(given_user, given_pwd):
        session["logged_in"] = given_user
        return redirect(url_for("home"))
    else:
        flash("Username or password is incorrect")
        return redirect(url_for("login"))

# attempts to add the user to the database
@app.route("/adduser")
def add_user():
    if(not request.args["user"].strip() or not request.args["password"] or not request.args["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))
    if(db.user_exist(request.args["user"])):
        flash("Username already taken")
        return redirect(url_for("register"))
    if(request.args["password"] != request.args["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))
    db.add_user(request.args["user"], request.args["password"], request.args["name"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))

# logs the user out and removes session
@app.route("/logout")
def logout():
	if session.get("logged_in"):
		session.pop("logged_in")
	return redirect(url_for("home"))

# if logged in, directs user to homepage
# if not logged in, directs to login page
@app.route("/home", methods = ["GET", "POST"])
def home():
    if "logged_in" in session:
        name = db.get_name(session["logged_in"])
        return render_template("home.html", title = "Home", heading = "Hello " + name + "!", user = session["logged_in"], name = name, logged_in = True)
    return redirect(url_for("login"))

# if logged in, directs user to finance tracker
# if not logged in, directs to login page
@app.route("/finance", methods = ["GET", "POST"])
def finance():
    if "logged_in" in session:
        name = db.get_name(session["logged_in"])
        records = db.get_records(session["logged_in"])
        cash = debit = venmo = 0
        if records != []:
            for each in records:
                if each[4] == "cash":
                    cash += each[3]
                elif each[4] == "debit":
                    debit += each[3]
                elif each[4] == "venmo":
                    venmo += each[3]
        return render_template("finance.html", title = "Finance", heading = "Finance", user = session["logged_in"], name = name, records = records, total = format(cash + debit + venmo, '.2f'), cash = cash, debit = debit, venmo = venmo, logged_in = True)
    return redirect(url_for("login"))

# updates user's financial records
@app.route("/update_records", methods = ["GET", "POST"])
def update_records():
    date = request.args["date"]
    description = request.args["description"]
    amount = request.args["amount"]
    mode = request.args["mode"]
    if request.args["update"] == "add":
        db.add_record(session["logged_in"], date, description, amount, mode)
    elif request.args["update"] == "remove":
        db.remove_record(session["logged_in"], date, description, amount, mode)
    return redirect(url_for("finance"))

# if logged in, directs user to settings
# if not logged in, directs to login page
@app.route("/settings", methods = ["GET", "POST"])
def settings():
    if "logged_in" in session:
        name = db.get_name(session["logged_in"])
        return render_template("settings.html", title = "Settings", heading = "Settings", user = session["logged_in"], name = name, logged_in = True)
    return redirect(url_for("login"))

if __name__ == "__main__":
        app.debug = True
        app.run()
