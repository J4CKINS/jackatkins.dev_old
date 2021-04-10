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

#database class
import mysql.connector
class Database:

    database = None
    cursor = None

    @staticmethod
    def connect():
        Database.database = mysql.connector.connect(
            host="jackatkins.dev",
            user="app",
            password="xLmNN^&099nm>",
            auth_plugin="mysql_native_password",
            database="jackatkins_dev",
            autocommit=True,
        )
        Database.cursor = Database.database.cursor()

    @staticmethod
    def disconnect():
        if Database.database:
            Database.database.close()
            Database.cursor.close()

# create app object
app = Flask(__name__)

# config app
app.secret_key = "SN1KT4196419662003"

#FOLDER PATHS

# this is needed because for some reason when the web app is run on apache
# it is ran at the root directory and not where the python file is
# which means that none of the resouces can be found
app_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(app_path,"static/img/")

# APP ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/", methods=["GET","POST"])
def blog():
    
    if request.method == "GET":

        Database.connect()

        # fetch posts from database
        Database.cursor.execute("SELECT * FROM tblBlogPosts WHERE posted = 1 ORDER BY datestamp DESC;")
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
            })
        

        return render_template("blog.html", posts=posts)


@app.route("/projects/", methods=["GET","POST"])
def projects():

    if request.method == "GET":

        Database.connect()

        # fetch posts from database
        Database.cursor.execute("SELECT * FROM tblProjectPosts WHERE posted = 1 ORDER BY datestamp DESC;")
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


@app.route("/image/")
def images():
    return render_template("images.html", images=os.listdir(image_path)) 


@app.route("/image/<name>")
def image(name):
    width = int(request.args.get('w'))
    height = int(request.args.get('h'))
    frmat = name.split(".")[1]

    image = Image.open(image_path + "/" + name)
    image = image.resize((width,height))

    return servePilImage(image,frmat)

# IMAGE UPLOAD API
@app.route("/upload_image/", methods=["POST"])
def upload_image():

    accepted_formats = ["png", "jpg", "jpeg", "gif", "bmp", "svg"]
    # get request data
    data = json.loads(request.data)

    # fetch auth key
    with open(os.path.join(app_path, "auth.txt"), "rb") as file:
        auth_key = file.read()

    #check if request is authorized
    if bcrypt.checkpw(data["auth"].encode(), auth_key):

        image_data = base64.b64decode(data["data"]) #decode image data

    if data["format"].lower() in accepted_formats:
        #write image data to file
        filename = data["filename"] + "." + data["format"]
        with open(os.path.join(image_path, filename), "w+") as file:
            file.write(image_data)
            
            return "200"
    else:
        abort(500)
    
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
        message = "Oops... An internal error has occurred"
    )

# functions

def convertMarkdown(data):
    return markdown.markdown(data, extensions=[FencedCodeExtension()])

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

def servePilImage(img, format):
    imgio = BytesIO()
    img.save(imgio, format.upper(), quality=70)
    imgio.seek(0)
    return send_file(imgio, mimetype='image/' + format.lower())

if __name__ == "__main__":
    app.run(host='0.0.0.0')