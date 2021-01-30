#general libs
from datetime import datetime
from bs4 import BeautifulSoup, Tag
import bcrypt
import requests
import json
import base64
import markdown

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
from flask import abort

#database class
from database import Database

# create app object
app = Flask(__name__)

# config app
app.secret_key = "SN1KT4196419662003"

# APP ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/", methods=["GET","POST"])
def blog():
    
    if request.method == "GET":

        Database.connect()

        # fetch posts from database
        Database.cursor.execute("SELECT * FROM tblBlogPosts ORDER BY timestamp DESC;")
        data = Database.cursor.fetchall()

        Database.disconnect()

        
        # put post data into list
        posts = list()
        for post in data:

            #format datestamp
            datestamp   = post[3]
            day         = datestamp.strftime("%d")
            month       = datestamp.strftime("%m")
            year        = datestamp.strftime("%Y")

            date = day + "-" + month + "-" + year

            posts.append({
                "title": post[1],
                "content": highlightCode(convertMarkdown(post[2])),
                "datestamp": date,
                "posted": bool(int(post[4]))
            })
        

        return render_template("blog.html", posts=posts)


@app.route("/projects/", methods=["GET","POST"])
def projects():

    if request.method == "GET":

        Database.connect()

        # fetch posts from database
        Database.cursor.execute("SELECT * FROM tblProjectPosts ORDER BY timestamp DESC;")
        data = Database.cursor.fetchall()

        Database.disconnect()
    
        # put post data into list
        posts = list()
        for post in data:

            #format datestamp 
            datestamp   = post[3]
            day         = datestamp.strftime("%d")
            month       = datestamp.strftime("%m")
            year        = datestamp.strftime("%Y")

            date = day + "-" + month + "-" + year

            posts.append({
                "ID": str(post[0]),
                "title": post[1],
                "content": highlightCode(convertMarkdown(post[2])),
                "datestamp": date,
                "posted": bool(int(post[4]))
            })

        return render_template("projects.html", posts=posts)

@app.route("/projects/<ID>/")
def project(ID):

    Database.connect()

    # get post from database
    Database.cursor.execute("SELECT * FROM tblProjectPosts WHERE id = " + str(ID)  + " AND posted = 1;")
    data = Database.cursor.fetchone()

    Database.disconnect()

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


@app.route("/image/<name>")
def image(name):
    return send_from_directory('static/img', name)

# IMAGE UPLOAD API
@app.route("/upload_image/", methods=["POST"])
def upload_image():

    # get request data
    data = json.loads(request.data)

    # fetch auth key
    with open("static/auth/auth.txt", "rb") as file:
        auth_key = file.read()

    #check if request is authorized
    if bcrypt.checkpw(data["auth"].encode(), auth_key):

        image_data = base64.b64decode(data["data"]) #decode image data
        
        #write image data to file
        with open(("static/img/" + data["filename"] + "." + data["format"]), "wb") as file:
            file.write(image_data)
        
        return "200"
    
    abort(403)



#WOTW
@app.route("/emma/")
def wotw():
    return render_template("wotw.html")


# ERROR HANDLING
@app.errorhandler(404)
def Error404(e):
    return render_template(
        "error.html",
        error = "404",
        message = "Sorry, we couldn't find what you were looking for :("
    )

@app.errorhandler(403)
def Error403(e):
    return render_template(
        "error.html",
        error = "403",
        message = "Sorry, you are not allowed to access this resource."
    )

@app.errorhandler(500)
def Error505(e):
    return render_template(
        "error.html",
        error = "500",
        message = "Oops... An internal error has ocDatabase.cursored."
    )

# functions

def convertMarkdown(data):
    return markdown.markdown(data, extensions=[FencedCodeExtension()])

def getLexer(name):

    #need to split the name first because its formatted like this: language-[language]
    #print("\n\n" + str(name) + "\n\n")
    #name = name.split("-")[1]
    return get_lexer_for_filename(("." + name))


def highlightCode(post):

    soup = BeautifulSoup(post, 'html.parser') # create new soup instance for html parsing

    # find all of the code tags in the content and sdve them to a list
    codeTags = soup.findAll("code")

    # highlight code contained in tags and save to separate list
    highlightedCode = []
    for code in codeTags:
        
        # incase the user forgot to specify the code block language in the markdown
        if code.has_key("class"):
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

if __name__ == "__main__":
    app.run()
