import bcrypt
import uuid

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
        if authenticateUser(request.form['user'], request.form['password']):
            return redirect(url_for("postit.home"))

        return redirect(url_for("home"))


# Functions
def authenticateUser(username, password):
    # Get user account data from database
    Database.connect()
    data = Database.getUserAccount(username)
    Database.disconnect()

    # check if any data has been found
    if data:
        # check if password entered matched password hash stored on database
        if bcrypt.checkpw(password.encode(), data[2].encode()):
            session['auth'] = genToken(data[0]) # Gen a new token for the user and save to session data
            return True # return that authentication was successful

    return False # authentication was not successful

def genToken(userID):
    token = str(uuid.uuid4())
    Database.updateUserToken(userID, token)
    return token