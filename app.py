from datetime import datetime
import bcrypt

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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#MODELS
class AdminAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class ProjectPost(db.Model):
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
    try:
        if session["admin_user"]:
            return render_template("admin.html")
    except KeyError:
        return redirect(url_for("home"))

@app.route("/admin/login/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        
        # get data from form
        username = request.form["user"]
        password = request.form["pass"]

        # get username and password from database
        account = AdminAccount.query.filter_by(username=username).first()

        # if account name not found
        if account is None:
            return redirect(url_for("home")) # redirect user

        # compare entered password and account password
        if bcrypt.checkpw(password.encode(), account.password.encode()):
            #login successful
            session["admin_user"] = account.username
            return redirect(url_for("admin"))

        else:
            return redirect(url_for("home"))

    else:
        return render_template("login.html")

@app.route("/admin/blog/newpost/", methods=["GET","POST"])
def newblogpost():
    return render_template("newblogpost.html")

if __name__ == "__main__":
    app.run()

