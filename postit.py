import bcrypt

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import session

from database import Database

postit = Blueprint(
    'postit',
    __name__,
    subdomain="postit",
    static_folder="./static",
    template_folder="./templates"
)

#ROUTES

@postit.route("/")
def home():
    if 'auth' in session:
        return "dashboard"
    else:
        return redirect(url_for("postit.login"))

@postit.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("postit/login.html")
    else:
        return str(authenticateUser(request.form['user'], request.form['password']))


# Functions
def authenticateUser(username, password):
    # Get user account data from database
    Database.connect()
    data = Database.getUserAccount(username)
    Database.disconnect()

    # Return if password entered matched password hash stored on database
    return bcrypt.checkpw(password.encode(), data[2].encode())
        
    