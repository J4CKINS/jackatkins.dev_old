from datetime import datetime

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask import request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#MODELS
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

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

@app.route("/admin/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # GET FORM DATA AND STUFF
        pass

@app.route("/admin/blog/newpost/", methods=["GET","POST"])
def newblogpost():
    return render_template("newblogpost.html")

if __name__ == "__main__":
    app.run()

