#general libs
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from PIL import Image
from io import BytesIO
import bcrypt
import requests
import json
import base64
import markdown
import os
import uuid

#markdown extensions
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

# code highlighting
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

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

from database import Database

#PostIT API
from postit import postit

from gallery import gallery

# create app object
app = Flask(__name__)
app.register_blueprint(gallery)

app.register_blueprint(postit)

# config app
app.secret_key = b"50de4b4c-760c-4249-b466-5497659e0954"

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

@app.route("/blog/", methods=["GET","POST"])
def blog():
    
    if request.method == "GET":

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
                highlightCode(convertMarkdown(post[2])),
                date,
            ])
        

        return render_template("blog.html", posts=posts)


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

    data = Database.getProjectPostByID(ID)

    if data != None:
        #format datestamp 
        datestamp   = data[3]
        day         = datestamp.strftime("%d")
        month       = datestamp.strftime("%m")
        year        = datestamp.strftime("%Y")

        date = day + "-" + month + "-" + year

        # append data to dict
        post = {
            "title":data[1],
            "content":highlightCode(convertMarkdown(data[2])),
            "datestamp":date
        }

        return render_template("project.html", post=post)
    
    # no post found
    else:
        abort(404)

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

# functions
# MARKDOWN CONVERTER
def convertMarkdown(data):
    return markdown.markdown(data, extensions=[FencedCodeExtension()])

# CODE HIGHLIGHTING
def getLexer(name):

    #need to split the name first because its formatted like this: language-[language]
    try:
        name = name.split("-")[1]
        return get_lexer_for_filename(("." + name))

    # for some reason the value of name is sometimes: language-py
    # and sometimes it is just py
    # this is handled here
    except IndexError:
        return get_lexer_for_filename(("." + name))
    
    # if the lexer is not specified in the markdown or cannot be found
    except:
        return get_lexer_for_filename(".txt")


def highlightCode(post):

    soup = BeautifulSoup(post, 'html.parser') # create new soup instance for html parsing

    # find all of the code tags in the content and sdve them to a list
    codeTags = soup.findAll("code")

    # highlight code contained in tags and save to separate list
    highlightedCode = []
    for code in codeTags:
        
        # incase the user forgot to specify the code block language in the markdown
        if code.has_attr("class"):
            lexer = getLexer(code["class"][0])
        else:
            lexer = getLexer("language-txt") # if no language is specified use a txt lexer

        highlightedCode.append(highlight(code.text, lexer, HtmlFormatter(linenos=False))) #TODO add multilexer support
    
    #insert formatted code into their own soup objects
    codeSoups = []
    for code in highlightedCode:
        codeSoups.append(BeautifulSoup(code, 'html.parser'))

    # clear main soup code tags for formatted code to be inserted into
    for tag in codeTags:
        tag.clear()
    
    # insert code from codeSoups into main soup code tags
    for index, tag in enumerate(soup.findAll("code")):
        tag.insert(1, codeSoups[index])
    
    #and finalyyyyy.... return soup
    return soup
