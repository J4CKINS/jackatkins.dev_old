from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#models
from models import BlogPost

#APP CONFIG
app.secret_key = "SN1KT4196419662003"

# MAIN ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/")
def blog():
    return render_template("blog.html")

@app.route("/projects/")
def projects():
    return render_template("projects.html")


#ADMIN PAGE ROUTES

@app.route("/admin/")
def admin():
    return render_template("admin.html")

@app.route("/admin/blog/newpost/")
def newblogpost():
    return render_template("newblogpost.html")

if __name__ == "__main__":
    app.run()

