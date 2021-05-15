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
from guard import Guard

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
    
    if 'auth' in session and 'id' in session:
        if Guard.authenticateUserToken(session['id'], session['auth']):
            return "dashboard"

    return redirect(url_for("postit.login"))

@postit.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("postit/login.html")
    
    # Handle post request
    else:
        auth = Guard.authenticateUser(
            request.form['user'],
            request.form['password']
        )

        if auth:
            session['id'] = auth[0]
            session['auth'] = auth[1]

            

            return redirect(url_for('postit.home'))

        return redirect(url_for("home")) # if user cannot be authenticated, redirect to home page