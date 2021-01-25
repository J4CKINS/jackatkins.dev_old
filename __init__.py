#TODO
#   create API for posting
#   Implement markdown converter
#________________________________________________________________________


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
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

#flask libs
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import send_from_directory

#mysql libs and setup
import mysql.connector
database = mysql.connector.connect(
    host="jackatkins.dev",
    user="app",
    password="F9we7t4f",
    database="site_database",
    autocommit=True
)
cur = database.cursor()

# create app object
app = Flask(__name__)

# config app
app.secret_key = "SN1KT4196419662003"
auth = "Ds9k74t3"

# APP ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/", methods=["GET","POST"])
def blog():
    
    if request.method == "GET":

        # fetch posts from database
        cur.execute("SELECT * FROM tblBlogPosts ORDER BY timestamp DESC;")
        data = cur.fetchall()
        
        # put post data into list
        posts = list()
        for post in data:
            posts.append({
                "title": post[1],
                "content": highlightCode(convertMarkdown(post[2])),
                "datestamp": post[3],
                "posted": bool(int(post[4]))
            })
        

        return render_template("blog.html", posts=posts)


@app.route("/projects/", methods=["GET","POST"])
def projects():

    if request.method == "GET":

        # fetch posts from database
        cur.execute("SELECT * FROM tblProjectPosts ORDER BY timestamp DESC;")
        data = cur.fetchall()
    
        # put post data into list
        posts = list()
        for post in data:
            posts.append({"title":post[1], "content":markdown.markdown(post[2]), "datestamp":post[3], "posted":bool(post[4])})

        return render_template("projects.html", posts=posts)

@app.route("/image/<name>")
def image(name):
    return send_from_directory('static/img', name)

# IMAGE UPLOAD API
@app.route("/upload_image/", methods=["POST"])
def upload_image():

    # get request data
    data = json.loads(request.data)

    # fetch auth key
    with open("static/auth/auth.txt", "r") as file:
        auth_key = file.read()

    #check if request is authorized
    if auth_key == data["auth"]:

        image_data = base64.b64decode(data["data"]) #decode image data
        
        #write image data to file
        with open(("static/img/" + data["filename"] + "." + data["format"]), "wb") as file:
            file.write(image_data)
        
        return "200"
    
    return "403"



#WOTW
@app.route("/emma/")
def wotw():
    return render_template("wotw.html")


def convertMarkdown(data):
    return markdown.markdown(data, extensions=[FencedCodeExtension(), CodeHiliteExtension()])

def highlightCode(post):

    soup = BeautifulSoup(post, 'html.parser') # create new soup instance for html parsing

    # find all of the code tags in the content and sdve them to a list
    codeTags = soup.findAll("code")

    # highlight code contained in tags and save to separate list
    highlightedCode = []
    for code in codeTags:
        highlightedCode.append(highlight(code.text, PythonLexer(), HtmlFormatter())) #TODO add multilexer support
    
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
    app.run(debug=True)