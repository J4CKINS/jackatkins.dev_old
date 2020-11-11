from datetime import datetime
import bcrypt
import requests
import json

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import session
from flask import request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#SQLALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

#MODELS
class AdminAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

class ProjectPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

#APP CONFIG
app.secret_key = "SN1KT4196419662003"

# MAIN ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/")
def blog():

    # get blog posts from database
    posts = BlogPost.query.all()

    return render_template("blog.html", posts=posts)

@app.route("/projects/")
def projects():
    return render_template("projects.html")


#ADMIN PAGE ROUTES

@app.route("/admin/")
def admin():
    try:
        if session["admin_user"]:
            return render_template("admin.html")
    except KeyError:
        return redirect(url_for("login"))


@app.route("/admin/login/", methods=["GET","POST"])
def login():

    # LOGIN REQUEST
    if request.method == "POST":
        
        # get data from form
        username = request.form["user"]
        password = request.form["pass"]

        # get username and password from database
        account = AdminAccount.query.filter_by(username=username).first()

        # if account name not found
        if account is None:
            return redirect(url_for("home")) # redirect user

        # compare entered password and account password
        if bcrypt.checkpw(password.encode(), account.password.encode()):
            #login successful
            session["admin_user"] = account.username
            return redirect(url_for("admin"))

        else:
            return redirect(url_for("home"))

    else:
        return render_template("login.html")
        

@app.route("/admin/blog/newpost/", methods=["GET","POST"])
def newblogpost():

    if request.method == "POST":
        
        # validate user
        try:
            if session["admin_user"]:
                
                # get form data
                title = request.form["title"]
                content = request.form["content"]

                # add blog post to database
                post = BlogPost(created=datetime.now(), title=title, content=content)
                db.session.add(post)
                db.session.commit()

                # redirect to the blog page
                return redirect(url_for("blog"))

        except KeyError:
            return redirect(url_for("login"))

    else:
        # check if admin is logged in
        try:
            if session["admin_user"]:
                return render_template("newblogpost.html")
        except KeyError:
            return redirect(url_for("login"))



@app.route("/admin/blog/posts/")
def blogposts():
    
    #validate user
    try:
        if session["admin_user"]:
            
            #load posts from database
            posts = BlogPost.query.all()

            return render_template("blogposts.html", posts=posts)

    except KeyError:
        return redirect(url_for("login"))


@app.route("/admin/blog/posts/edit/<id>/", methods=["GET", "POST"])
def editpost(id):

    #validate user
    try:
        if session["admin_user"]:

            if request.method == "POST":
                
                # get form data
                title = request.form["title"]
                content = request.form["content"]

                # get record that needs to be updated
                post = BlogPost.query.filter_by(id=id).first()

                if post:
                    post.title = title
                    post.content = content
                    db.session.commit()

                    return redirect(url_for("blogposts"))
                
                else:
                    return redirect(url_for("blogposts"))
            
            else:
                
                #load post data from database
                post = BlogPost.query.filter_by(id=id).first()

                # if post exists
                if post:
                    return render_template("editpost.html", post=post)
                else:
                    return redirect(url_for("blogposts"))

    except KeyError:
        return redirect(url_for("login"))


@app.route("/admin/blog/posts/delete/<id>/")
def deletepost(id):

    # validate user
    try:
        if session["admin_user"]:

            # get record from database
            post = BlogPost.query.filter_by(id=id).first()

            if post:
                # delete post
                db.session.delete(post)
                db.session.commit()

                return redirect(url_for("blogposts"))

            else:
                return redirect(url_for("blogposts"))

    except:
        return "403"


@app.route("/admin/imageupload/", methods=["POST"])
def imageupload():

    #verify user
    try:
        if session["admin_user"]:
            
            #send data off to imgur api
            payload = {"image": request.data.decode()}
            headers = {'Authorization': 'Client-ID 78182536f30f0fe'}
            res = requests.request("POST", "https://api.imgur.com/3/image", headers=headers, data=payload, files=[])

            res = json.loads(res.text.encode('utf8').decode())

            if res["success"]:
                return res["data"]["link"]
            else:
                return res["success"] + " Error connecting to API"

    except KeyError:
        return "403"

if __name__ == "__main__":
    db.create_all()
    app.run()

