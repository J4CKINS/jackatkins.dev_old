import bcrypt
import uuid
import functools
import datetime

from styler import convertMarkdown
from styler import highlightCode

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import session
from flask import make_response

from database import Database
from guard import Guard

postit = Blueprint(
    'postit',
    __name__,
    url_prefix="/postit",
    static_folder="./static",
    template_folder="./templates"
)

# PROTECTED ENDPOINTS DECORATOR
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if 'auth' in session and 'id' in session:
            if Guard.authenticateUserToken(session['id'], session['auth']):
                return func(*args, **kwargs)
        return redirect(url_for('postit.login', next=request.url))

    return secure_function


#ROUTES

@postit.route("/")
def home():
    return redirect(url_for('postit.dashboard', postType='blog'))

@postit.route("/dashboard/<postType>/")
@login_required
def dashboard(postType):

    # Get the blog posts from database
    if postType == "blog":
        posts = Database.getBlogPosts()

    # Get the project posts from the database
    elif postType == "projects":
        posts = Database.getProjectPosts()
    
    # Something else has been entered in as postType
    else:
        # Try to guess what post type the user wants by looking at the first letter of url post type
        if postType[0].lower() == "p":
            # if postType starts with char: p, return project posts dashboard
            return redirect(url_for('postit.dashboard', postType='projects'))
        
        # return blog posts by default
        return redirect(url_for('postit.dashboard', postType='blog'))
    
    return render_template('postit/dashboard.html', posts=posts, postType=postType)

@postit.route("editor/<postType>/<postID>/", methods=['GET', 'POST'])
@login_required
def editor(postType, postID):

    #incorrect spelling in post type has ocurred
    # this needs to be corrected
    if postType != "projects" or postType != "blog":
        if postType[0].lower() == "p": postType = "projects"
        else: postType = "blog"

    # Route has received a GET request
    if request.method == "GET":
 
        # Check if post is new or being edited 
        if postID != "0":
            # get post data
            if postType == "blog":
                post = Database.getBlogPostByID(postID)
            
            else:
                post = Database.getProjectPostByID(postID)
            
            # check if any data was found
            if post:
                title = post[1]
                content = post[2]
                posted = bool(post[4])
            
            # redirect to a new post if no data was found
            else:
                return redirect(url_for('postit.editor', postType=postType, postID=0))
        
        else:
            # if the post is new,
            # set the title, content, and posted variables to a default value
            title = ""
            content = ""
            posted = "off"
        return render_template('postit/editor.html', title=title, content=content, posted=posted)
        
    # Check if request is POST method
    elif request.method == "POST":
                
        # Get form data
        title = request.form['title']
        content = request.form['content']
        posted = request.form.get('posted', '0')
        posted = '1' if posted == 'on' else '0'

        # Check post type   
        if postType == "blog":

            # Check if post exists
            if not Database.blogPostExists(postID):
                postID = '0' # Set ID to 0 so a new post is created

            # Check if post is new
            if postID == '0':
                Database.createBlogPost(
                    title,
                    content,
                    posted
                )

            # If post is not new, modify an existing post
            else:
                Database.updateBlogPost(
                    postID,
                    title,
                    content,
                    posted
                )

        # Post type is project
        else:

            # Check if post exists
            if not Database.projectPostExists(postID):
                postID = '0'

            # Check if post is new
            if postID == '0':
                Database.createProjectPost(
                    title,
                    content,
                    posted
                )

            else:
                Database.updateProjectPost(
                    postID,
                    title,
                    content,
                    posted
                )

        return redirect(url_for('postit.dashboard', postType=postType))
                
@postit.route("/delete/<postType>/<postID>/")
@login_required
def delete(postType, postID):

    # Check post type
    if postType == "blog":
        Database.deleteBlogPost(postID)
    else:
        Database.deleteProjectPosts(postID)

    return redirect(url_for('postit.dashboard', postType=postType))


@postit.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("postit/login.html")
    
    # Handle post request
    else:
        next_url = request.form.get("next")
        auth = Guard.authenticateUser(
            request.form['user'],
            request.form['password']
        )

        if auth:
            session['id'] = auth[0]
            session['auth'] = auth[1]

            return redirect(next_url)

        return redirect(url_for('home')) # if user cannot be authenticated, redirect to dashboard page

@postit.route("/preview/", methods=["POST"])
@login_required
def preview():

    # get post title and content
    title = request.form.get("title","")
    content = highlightCode(convertMarkdown(request.form.get("content","")))
    date = datetime.date.today()

    return render_template('postit/post_preview.html', title=title, content=content, date=date)