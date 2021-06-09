import os
from flask import Flask, request, Markup, render_template
from datetime import datetime

app = Flask(__name__)

arch_pages = set()


@app.route("/Failure/")
def filter_info(con: str) -> tuple:
    # The idea is that since the three allowed tags all start the same
    # we can check the contents after a open brace is encountered to see
    # if it matches allowed tags
    # Currently brute-force gonna try to find library that does this better
    allowed = "<h1</h1<h2</h2<h3</h3<a></a<p></p"
    safe = True
    string = str(con)
    for i in range(len(con)):
        # If iterator encounters open bracket
        if con[i] == "<":
            # Check the next 2 letters to see if theyre in allowed
            if con[i : i + 2] not in allowed:
                safe = False
            # Markup.escape() changes all the HTML characters passed into
            # "safe" text
            if not safe:
                con = Markup.escape(con)
                return False, render_template(
                    "Failure.html",
                    page_name="Failed",
                    read_so_far=string[: string[i:].index(">") + i + 1],
                    issue=string[: string.index(">") + 1],
                    whole=string,
                )
    return True, con


@app.route("/")
def main():
    # For now, home page won't be able to be edited.
    found = os.listdir("pages")
    for page in found:
        arch_pages.add(page[:-4])
    arch_pages.remove("main")
    with open("pages/main.txt", "r") as f:
        contents = f.read()
    return render_template(
        "main.html",
        page_name="Front Page",
        page_content=Markup(contents),
        pages=arch_pages,
    )


@app.route("/create/", methods=["GET", "POST"])
def create_page():
    contents = ""
    page_name = request.form["new"]
    if page_name not in arch_pages:
        path = "pages/" + page_name + ".txt"
        contents = "<h1>" + page_name + "<h1>" + "<p>THIS IS A NEW PAGE</p>"
        with open(path, "w") as r:
            r.write(contents)
        status, con = filter_info(contents)
        if not status:
            return con
        return render_template(
            "test_page.html",
            page_name=page_name,
            contents=Markup(contents),
        )
    return get_page_name(page_name)


@app.route("/view/<page_name>")
def get_page_name(page_name: str) -> str:

    # Fullpath points to text file in pages,
    # template_path points to HTML template file

    fullpath = "pages/" + page_name + ".txt"
    # template_path = page_name + ".html"

    with open(fullpath, "r") as f:
        con = f.read()
    return render_template("test_page.html", page_name=page_name, contents=Markup(con))


@app.route("/edit-form/<page_name>")
def get_edit_form(page_name: str) -> str:
    # Plugs the text file's contents into a render template
    # for the given page
    with open("pages/" + page_name + ".txt", "r") as f:
        cc = f.read()
    return render_template("editform.html", current_contents=cc, page=page_name)


@app.route("/history/<page_name>")
def get_history(page_name):
    # Finds history page, if not found return a default template
    hist_path = "history/" + page_name + ".txt"
    content = []
    if os.path.exists(hist_path):
        with open(hist_path, "r") as r:
            raw = r.read()
        content = raw.split(":;:")
    return render_template("history.html", history=content)


@app.route("/edit/", methods=["GET", "POST"])
def edit_page():
    # Receives content and changes information from server
    page_name = request.form["page_name"]
    con = request.form["contents"]

    # Capture all change info into a single string
    edit_details = (
        "\n:;:Date: "
        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        + " |Author: "
        + request.form["Name"]
        + " |Email: "
        + request.form["Email"]
        + " |Change(s): "
        + request.form["changes"]
    )

    # check if history page exists and write or append the new changes
    hist_path = "history/" + page_name + ".txt"
    if os.path.exists(hist_path):
        with open(hist_path, "a") as w:
            w.write(edit_details)
    else:
        with open(hist_path, "w") as w:
            w.write(edit_details)

    # Variables for the text and html file path's for <page_name>
    fullpath = "pages/" + page_name + ".txt"
    template_path = page_name + ".html"

    status, con = filter_info(con)
    # Writes the changes to the text file
    if status:
        with open(fullpath, "w") as f:
            f.write(Markup(con))
    else:
        return con
    # Returns the template with filtered data
    return render_template(template_path, contents=Markup(con))
