from flask import Flask, flash, redirect, render_template, request, session
from helpers import apology
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmation")

    if not username:
        return apology("Missing username")

    if not password:
        return apology("Missing password")

    if not confirm_password:
        return apology("Missing password confirmation")

    if password != confirm_password:
        return apology("password does not match confirmation")

    # if username == db.execute("SELECT username FROM users"):
    #     return apology("Duplicate username")

    # try:
    #     id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
    # except ValueError:
    #     return apology("Error! Username is taken")

    # rows = db.execute("SELECT * FROM users WHERE username = ?", username)

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
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        #
        # # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #     return apology("invalid username and/or password", 403)
        #
        # # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/")
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run()
