from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask import abort
from flask import request

gallery = Blueprint(
    'gallery',
    __name__,
    static_folder="./static",
    template_folder="./templates",
    subdomain="gallery"
)

@gallery.route("/")
def home():
    return "gallery"