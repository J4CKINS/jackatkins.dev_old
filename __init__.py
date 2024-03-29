#general libs
from datetime import datetime
from PIL import Image
from io import BytesIO
import bcrypt
import requests
import json
import base64
import os
import uuid

#flask libs
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import send_file
from flask import abort
from flask import make_response

# Post Styling
from styler import convertMarkdown
from styler import highlightCode

# database
from database import Database

#PostIt API
from postit import postit

#PostIt Gallery
from gallery import gallery

# create app object
app = Flask(__name__)
app.register_blueprint(gallery)

app.register_blueprint(postit)

# config app
with open("app_key.txt", "r") as file:
    app.secret_key = file.read()

#FOLDER PATHS

# this is needed because for some reason when the web app is run on apache
# it is ran at the root directory and not where the python file is
# which means that none of the resouces can be found
app_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(app_path,"static/uploads/")

# APP ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/")
def blog():
    
    data = Database.getBlogPosts(postedOnly=True)

    # put post data into list
    posts = list()
    for post in data:

        #format datestamp
        day, month, year = Database.formatDatestamp(post[3])
        date = day + "-" + month + "-" + year
        
        posts.append([
            post[0],
            post[1],
            date,
        ])
    
    return render_template("blog.html", posts=posts)

@app.route("/blog/<ID>/")
def blog_post(ID):

    if Database.blogPostExists(ID, postedOnly=True):
        if request.args.get("raw_content") == "true" or request.args.get("raw_content") == "1":
            return str(
                highlightCode(
                    convertMarkdown(
                        Database.getBlogPostByID(ID)[2]
                    )
                )
            )
        
        else:
            post = [
                Database.getBlogPostByID(ID)[0],
                Database.getBlogPostByID(ID)[1],
                str(highlightCode(convertMarkdown(Database.getBlogPostByID(ID)[2]))),
                Database.getBlogPostByID(ID)[3],
            ]
            return render_template('blog_post.html', post=post)

    else: return abort(404)

@app.route("/projects/", methods=["GET","POST"])
def projects():

    if request.method == "GET":

        data = Database.getProjectPosts(postedOnly=True)
    
        # put post data into list
        posts = list()
        for post in data:

            #format datestamp 
            day, month, year = Database.formatDatestamp(post[3])
            date = day + "-" + month + "-" + year

            posts.append({
                "ID": str(post[0]),
                "title": post[1],
                "content": highlightCode(convertMarkdown(post[2])),
                "datestamp": date,
            })

        return render_template("projects.html", posts=posts)

@app.route("/projects/<ID>/")
def project(ID):

    if not Database.projectPostExists(ID, postedOnly=True): return abort(404)
    
    data = Database.getProjectPostByID(ID)

    day, month, year = Database.formatDatestamp(data[3])
    date = day + "-" + month + "-" + year

    # append data to dict
    post = {
        "title":data[1],
        "content":highlightCode(convertMarkdown(data[2])),
        "datestamp":date
    }

    return render_template("project.html", post=post)



#WOTW
@app.route("/emma/")
def wotw():
    return render_template("wotw.html")

#ROBOTS
@app.route("/robots.txt")
def robots():
    return send_file(app_path + "/robots.txt")



# ERROR HANDLING
@app.errorhandler(404)
def Error404(e):
    return make_response(render_template(
        "error.html",
        error = "404",
        message = "Sorry, we couldn't find what you were looking for :("
    ), 404)

@app.errorhandler(403)
def Error403(e):
    return make_response(render_template(
        "error.html",
        error = "403",
        message = "Sorry, you are not allowed to access this resource."
    ), 403)

@app.errorhandler(500)
def Error500(e):
    return make_response(render_template(
        "error.html",
        error = "500",
        message = "Oops... An internal error has occurred"
    ), 500)

