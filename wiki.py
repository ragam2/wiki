from flask import Flask,redirect, url_for
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main(page_name, page_content):
    return render_template(
        "main.html",
        page_name=page_name,
        page_content=page_content,
    )

@app.route("/view/")
def get_front_page():
    return redirect(url_for('get_page_name', page_name = "FrontPage"))

@app.route("/view/<page_name>")
def get_page_name(page_name):
    fullpath = "pages/" + page_name + ".txt"
    with open(fullpath, "r") as f:
        contents = f.read()
    
    return contents
