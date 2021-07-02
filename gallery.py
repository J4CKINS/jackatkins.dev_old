import os
import functools
import json
from io import BytesIO
from PIL import Image
import shutil

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask import abort
from flask import request
from flask import session
from flask import send_file
from flask import Response
from flask import make_response

from database import Database
from guard import Guard

app_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(app_path,"static", "uploads")

gallery = Blueprint(
    'gallery',
    __name__,
    template_folder="./templates",
    url_prefix="/gallery"
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


@gallery.route("/", defaults={'path':""})
@gallery.route("/<path:path>")
@login_required
def home(path):
    
    current_dir = request.args.get("current_dir","")
    try:
        return render_template("gallery/gallery.html", current_path=path, tree=getDirectoryList(os.path.join(image_path, path)))
    except FileNotFoundError: # The folder specified in the URL could not be found
        return abort(404)
    except NotADirectoryError: # The path specified is not a directory
        return redirect(url_for('gallery.image', path=path)) # Redirect to image route to serve image

@gallery.route("/upload/")
@login_required
def upload():
    return render_template("gallery/upload.html")

@gallery.route("/image/<path:path>/")
def image(path):
    
    # clamp is a function that is used to keep a value within a specified range
    # this is used for the URL args because PIL doesnt accept numbers (<=0)
    # I have written this as a lambda function as it looks cleaner
    clamp = lambda val,minimum,maximum : max(minimum, min(val, maximum))

    image = Image.open(os.path.join(image_path, path))

    # Get image format
    filename, frmat = os.path.splitext(path)
    frmat = frmat.strip(".")
    frmat = "jpeg" if frmat.upper() == "JPG" else frmat
    print(frmat)
    
    width = request.args.get("w", default=image.width, type=int)
    height = request.args.get("h", default=image.height, type=int)
    scale = request.args.get("scale", default=1, type=float)

    # Clamp values
    width = clamp(width, 1, 5000)
    height = clamp(height, 1, 5000)
    scale = clamp(scale, 0.01, 5)

    # resize the image
    image = image.resize((width, height))
    # scale image
    image = image.resize((int(width*scale), int(height*scale)))
    
    # Serve image using BytesIO
    imgbytes = BytesIO()
    image.save(imgbytes, frmat.upper(), quality=70)
    imgbytes.seek(0)
    return send_file(imgbytes, mimetype='image/' + frmat.lower())

def getDirectoryList(directory):
    # Get list of files and folders in a specified directory
    tree = {"images":[], "folders":{}}
    for file in os.listdir(directory):
        # test if the element is a file or a folder
        if os.path.isfile(os.path.join(directory, file)):
            tree["images"].append(file)
        else:
            # Use recursion to get folders inside folders
            tree["folders"][str(file)] = getDirectoryList(os.path.join(directory,file))
    return tree

@gallery.route("/new/image/", methods=["POST"])
@login_required
def new_image():
    path = request.form.get("path", "")
    filename = request.form.get("filename", None)
    fileformat = request.form.get("format", None)
    image = request.files.get('file', None)

    # check if all data is present
    if not filename or not fileformat or not image:
        return Response(status=500) # return app error response

    image.save(os.path.join(image_path, path, filename+"."+fileformat))
    return redirect(url_for('gallery.home'))

@gallery.route("/new/folder/<path:path>/", methods=["POST"])
@login_required
def new_folder(path):
    try:
        os.mkdir(os.path.join(image_path, path))
        return Response(status=200)
    except:
        return Response(status=200)

@gallery.route("/delete/image/<path:path>/", methods=['POST'])
@login_required
def delete_image(path):
    try:
        os.remove(os.path.join(image_path, path))
        return Response(status=200)
    except:
        return Response(status=500) # internal error

@gallery.route("/delete/folder/<path:path>/", methods=["POST"])
@login_required
def delete_folder(path):
    delete_items_in_folder(os.path.join(image_path, path))
    return Response(status=200)

def delete_items_in_folder(path):
    files = list()
    folders = list()

    #get files and folders
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            files.append(os.path.join(path,item))
        else:
            folders.append(os.path.join(path,item))

    #delete images
    for file in files:
        os.remove(file)

    for folder in folders:
        delete_items_in_folder(folder)
        os.rmdir(folder)

    os.rmdir(path)