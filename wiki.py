from flask import Flask,redirect, url_for
from flask import request,Markup
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template(
        "main.html",
        page_name="Front Page",
        page_content="Welcome to Arch's Frontpage!"
    )

@app.route("/view/")
def get_front_page():
    # return redirect(url_for('get_page_name', page_name = "FrontPage"))
      return render_template(
        "main.html",
        page_name="Front Page",
        page_content="Welcome to Arch's Frontpage!"
    )


@app.route("/view/<page_name>")
def get_page_name(page_name):
    fullpath = "pages/" + page_name + ".txt"
    with open(fullpath, "r") as f:
        contents = f.read()
    
    return contents

@app.route("/view/page-edit-form")
def get_edit_form():
    with open("templates/FrontPage.html", "r") as f:
        cc = f.read()
    return render_template(
        "pageform.html",
        current_contents=cc
    )

@app.route("/view/handle-page-edits", methods=["GET", "POST"])
def edit_page():
    con = request.form["contents"]
    cha = request.form["changes"]
    page_name = request.form["name"]
    fullpath = "pages/" + page_name + ".txt"
    with open(fullpath, "w") as f:
        f.write(con)
    #with open("pages/EditPage.txt", "r") as f:
    return render_template(
        "FrontPage.html",
        contents=Markup(con)
    )
