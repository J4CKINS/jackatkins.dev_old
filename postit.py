from flask import Blueprint
from flask import render_template
from flask import request
from flask import abort

postit = Blueprint(
    'postit',
    __name__,
    subdomain="postit",
    static_folder="./static",
    template_folder="./templates"
)

@postit.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("postit/login.html")
