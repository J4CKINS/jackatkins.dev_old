from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/blog/")
def blog():
    return render_template("blog.html")

@app.route("/projects/")
def projects():
    return render_template("projects.html")

if __name__ == "__main__":
    app.run()

