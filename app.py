from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()