from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_new")
def login_new():
    return render_template("login_new.html")

@app.route("/add_exercise")
def add_exercise():
    return render_template("add_exercise.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")
    
if __name__ == "__main__":
    app.run(debug=True)
