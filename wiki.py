from flask import Flask,redirect
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    # Redirects to front page
    return redirect("/view/")

@app.route("/view/")
def get_frontpage():
    with open("pages/FrontPage.txt", "r") as f:
        contents = f.read()
    return render_template(
        "main.html",
        page_name="Front Page",
        page_content=contents,
    )

@app.route("/view/<pagename>")
def get_pagename(pagename):
    fullpath = "pages/" + pagename + ".txt"
    with open(fullpath, "r") as f:
        pn = f.read()
    
    return render_template(
        "main.html",
        page_name=pagename,
        page_content=pn,
    )
