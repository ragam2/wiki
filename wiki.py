from flask import Flask, request, Markup, render_template
from django.utils.html import strip_tags
from datetime import datetime
import os

app = Flask(__name__)

arch_pages = set()


def filter_info(con: str) -> tuple:
    # The idea is that since the three allowed tags all start the same
    # we can check the contents after a open brace is encountered to see
    # if it matches allowed tags
    # Currently brute-force gonna try to find library that does this better
    allowed = "<h1</h1<h2</h2<h3</h3<a></a<p></p<img<br"
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
                    issue="<script>",
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
    page_name = page_name.replace(" ", "_")

    if page_name not in arch_pages:
        path = "pages/" + page_name + ".txt"
        contents = "<h1>" + page_name + "</h1>" + "<p>THIS IS A NEW PAGE</p>"
        with open(path, "w") as r:
            r.write(contents)
        status, con = filter_info(contents)
        if not status:
            return con
        return render_template(
            "editform.html",
            page=page_name,
            contents=Markup(contents),
        )
    return get_page_name(page_name)


@app.route("/view/<page_name>")
def get_page_name(page_name: str) -> str:

    # Fullpath points to text file in pages,
    # template_path points to HTML template file

    fullpath = "pages/" + page_name + ".txt"
    if os.path.exists(fullpath):
        with open(fullpath, "r") as f:
            con = f.read()
        return render_template("page.html", page_name=page_name, contents=Markup(con))
    return main()


@app.route("/edit-form/<page_name>", methods=["GET", "POST"])
def get_edit_form(page_name):
    # Plugs the text file's contents into a render template
    # for the given page
    # page_name = request.form["page_name"]
    with open("pages/" + page_name + ".txt", "r") as f:
        cc = f.read()
    return render_template("editform.html", current_contents=cc, page=page_name)


@app.route("/history/<page_name>")
def get_history(page_name):
    # Finds history page, if not found return a default template
    # page_name = request.form["page_name"]
    hist_path = "history/" + page_name + ".txt"
    content = []
    if os.path.exists(hist_path):
        with open(hist_path, "r") as r:
            raw = r.read()
        content = raw.split(":;:")
    return render_template("history.html", history=content, page=page_name)


@app.route("/edit/<page_name>", methods=["GET", "POST"])
def edit_page(page_name):
    # Receives content and changes information from server
    # page_name = request.form["page_name"]
    con = request.form["contents"]
    changes = request.form["changes"]
    editor_name = request.form["Name"]
    email = request.form["Email"]

    if changes and editor_name and email:
        if "@" not in email or " " in email:
            return render_template(
                "editform.html",
                current_contents=Markup(con),
                page=page_name,
                error=Markup(
                    "<script>window.alert('Email content is not valid')</script>"
                ),
            )
        # Capture all change info into a single string
        edit_details = (
            "\n:;:Date: "
            + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            + " |Author: "
            + editor_name
            + " |Email: "
            + email
            + " |Change(s): "
            + changes
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

        status, con = filter_info(con)
        # Writes the changes to the text file
        if status:
            with open(fullpath, "w") as f:
                f.write(Markup(con))
        else:
            return con

        # Returns the template with filtered data
        return render_template(
            "page.html",
            contents=Markup(con),
            page_name=page_name,
        )
    else:
        return render_template(
            "editform.html",
            current_contents=Markup(con),
            page=page_name,
            error=Markup(
                "<script>window.alert('Remember to fill in all fields!')</script>"
            ),
        )


@app.route("/api/v1/page/<page_name>/get")
def page_api_get(page_name):
    format = request.args.get("format", "all")
    fullpath = "pages/" + page_name + ".txt"

    if not os.path.isfile(fullpath):
        json_response = {"success": False, "reason": "Page Not found"}
        status_code = 404
        return json_response, status_code

    with open(fullpath, "r") as f:
        cc = f.read()
    json_response = {}
    status_code = 0

    if format == "html":
        status_code = 200
        json_response["success"] = True
        json_response[format] = cc
    elif format == "raw":
        status_code = 200
        json_response["success"] = True
        json_response[format] = strip_tags(cc)
    elif format == "all":
        status_code = 200
        json_response["success"] = True
        json_response["html"] = cc
        json_response["raw"] = strip_tags(cc)
    else:
        status_code = 400
        json_response["success"] = False
        json_response["reason"] = "Unsupported format"
    return json_response, status_code
