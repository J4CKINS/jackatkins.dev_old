from flask import Blueprint
from flask import abort

postit = Blueprint(
    'postit',
    __name__,
    subdomain="postit",
    static_folder="./static",
    template_folder="./templates"
)

@postit.route("/")
def home():
    return "<h1>Wellcome to PostIt</h1>"
