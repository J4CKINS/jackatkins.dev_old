#TODO
#   create API for posting
#   Implement markdown converter
#________________________________________________________________________


#general libs
from datetime import datetime
import bcrypt
import requests
import json
import base64

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
    database="site_database"
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
            posts.append({"title":post[1], "content":post[2], "datestamp":post[3], "posted":bool(int(post[4]))})

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
            posts.append({"title":post[1], "content":post[2], "datestamp":post[3], "posted":bool(post[4])})

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


if __name__ == "__main__":
    app.run(debug=True)