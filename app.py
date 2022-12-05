import os
from flask import Flask, flash, redirect, render_template, request, session
from helpers import apology, login_required
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///courses.db")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmation")
    admin = request.form.get("admin")

    if not username:
        return apology("Missing username")

    if not password:
        return apology("Missing password")

    if not confirm_password:
        return apology("Missing password confirmation")

    if password != confirm_password:
        return apology("password does not match confirmation")

    if username == db.execute("SELECT username FROM users"):
        return apology("Duplicate username")

    if admin == "admin":
        try:
            id = db.execute("INSERT INTO users (username, hash, Admin) VALUES(?, ?, 1)", username, generate_password_hash(password))
        except ValueError:
            return apology("Error! Username is taken")
    else:
        try:
            id = db.execute("INSERT INTO users (username, hash, Admin) VALUES(?, ?, 0)", username, generate_password_hash(password))
        except ValueError:
            return apology("Error! Username is taken")

    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    session["user_id"] = id

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)



        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # # Remember which user has logged in
        session["user_id"] = rows[0]["id"]


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/", methods=['POST', 'GET'])
@login_required
def dashboard():

    user_id = session["user_id"]
    if request.method == "POST":
        value = request.form.get("clarinets")
        unvalue = request.form.get("unregister")
        if request.form.get("clarinets"):
            db.execute("INSERT INTO registered_courses (course_name, user_id) VALUES(?, ?)", value, user_id)
        elif unvalue:
            db.execute("DELETE FROM registered_courses WHERE course_name= ?", unvalue)

    user_id = session["user_id"]
    flag = db.execute("Select Admin From users Where id = ?", user_id)[0]["Admin"]


    submitted_courses = db.execute("SELECT * FROM available_courses WHERE course_name IN (SELECT course_name FROM registered_courses WHERE user_id = ?)", user_id)

    courses = db.execute("SELECT course_name FROM available_courses WHERE course_name NOT IN (SELECT course_name FROM registered_courses WHERE user_id = ?)",
        user_id)

    return render_template("dashboard.html", available_courses=courses, registered_courses=submitted_courses, flag = flag)


@app.route("/add", methods=['POST', 'GET'])
@login_required
def add():

    user_id = session["user_id"]
    if request.method == "POST":
        course_name = request.form.get("course_name")
        description = request.form.get("description")
        if course_name and description:
            db.execute("INSERT INTO available_courses (course_name, description) VALUES(?, ?)", course_name, description)
        elif not course_name:
            return apology("must provide course name", 403)
        elif not description:
            return apology("must provide description", 403)

    return render_template("add.html")


@app.route("/available", methods=['POST', 'GET'])
@login_required
def available():

    user_id = session["user_id"]
    if request.method == "POST":

        course = request.form.get("button")

        if course:
            db.execute("INSERT INTO registered_courses (user_id, course_name) VALUES(?,?)", user_id, course)
    flag = db.execute("Select Admin From users Where id = ?", user_id)[0]["Admin"]
    available_courses = db.execute("SELECT * FROM available_courses")
    return render_template("available.html", available_courses=available_courses, flag = flag)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()