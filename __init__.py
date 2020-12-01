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

    # get posts from database
    posts = ProjectPost.query.all()

    return render_template("projects.html", posts=posts)


#WOTW
@app.route("/emma/")
def emma():
    return render_template("wotw.html")


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
        

# POSTS
@app.route("/admin/<type>/post/<id>", methods=["GET","POST"])
def posteditor(type, id):

    # validate user
    try:
        if session["admin_user"]:

            # POST
            if request.method == "POST":

                title = request.form["title"]
                content = request.form["content"]

                if type == "blog":

                    if id == "new":
                        post = BlogPost(title=title, content=content, created=datetime.now())
                        db.session.add(post)
                        db.session.commit()

                    elif isinstance(id, int):
                        post = BlogPost.query.filter_by(id=id).first()

                        post.title = title
                        post.content = content

                        db.session.commit()

                    else:
                        return "404"
                    
                    return redirect(url_for("posts", type="blog"))


                elif type == "project":
                    if id == "new":
                        post = ProjectPost(title=title, content=content, created=datetime.now())
                        db.session.add(post)
                        db.session.commit()

                    elif isinstance(id, int):
                        post = ProjectPost.query.filter_by(id=id).first()

                        post.title = title
                        post.content = content

                        db.session.commit()

                    else:
                        return "404"

                else:
                    return "404"

            # GET
            else:
                
                # create a new post
                if id == "new":
                    if type == "blog":
                        return render_template("posteditor.html", postTitle="", postContent="")

                    elif type == "project":
                        return render_template("posteditor.html", postTitle="", postContent="" )
                    
                    else:
                        return "404"
                
                # edit post
                elif isinstance(int(id), int):
                    
                    post = None
                    if type == "blog":
                         post = BlogPost.query.filter_by(id=int(id)).first()
                    elif type == "project":
                        post = ProjectPost.query.filter_by(id=int(id)).first()
                    
                    if post:
                        return render_template("posteditor.html", postTitle=post.title, postContent=post.content)
                    
                    else:
                        return redirect(url_for("posts", type="projects"))

                # error
                else:
                    return "404"

    
    except KeyError:
        return redirect(url_for("login"))



@app.route("/admin/<type>/posts/")
def posts(type):

    # validate user
    try:
        if session["admin_user"]:

            if type == "blog":
                posts = BlogPost.query.all()
            elif type == "projects":
                posts = ProjectPost.query.all()
            else:
                return redirect(url_for("admin"))
            
            return render_template("posts.html", posts=posts, type=type.capitalize())
    
    except KeyError:
        return redirect(url_for("login"))



@app.route("/admin/blog/posts/delete/<id>/")
def deleteblogpost(id):

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



@app.route("/admin/projects/posts/delete/<id>")
def deleteprojectpost(id):

    # validate user
    try:
        if session["admin_user"]:

            # get post from database
            post = ProjectPost.query.filter_by(id=id).first()

            if post:
                db.session.delete(post)
                db.session.commit()

                return redirect(url_for("projectposts"))

            else:
                return redirect(url_for("projectposts"))

    except KeyError:
        return redirect(url_for("login"))


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

