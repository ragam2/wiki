from flask import Flask
from flask import request, Markup, render_template

app = Flask(__name__)


def filter_info(con: str) -> str:
    # The idea is that since the three allowed tags all start the same
    # we can check the contents after a open brace is encountered to see
    # if it matches allowed tags
    # Currently brute-force gonna try to find library that does this better
    allowed = "<h1</h1<h2</h2<h3</h3<a></a<p></p"
    safe = True
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
                break
    return con


@app.route("/")
def main():
    # For now, home page won't be able to be edited.
    with open("pages/main.txt", "r") as f:
        contents = f.read()
    return render_template(
        "main.html", page_name="Front Page", page_content=Markup(contents)
    )


@app.route("/view/<page_name>")
def get_page_name(page_name: str) -> str:

    # Fullpath points to text file in pages,
    # template_path points to HTML template file

    fullpath = "pages/" + page_name + ".txt"
    template_path = page_name + ".html"
    with open(fullpath, "r") as f:
        con = f.read()

    return render_template(template_path, contents=Markup(con))


@app.route("/edit-form/<page_name>")
def get_edit_form(page_name: str) -> str:
    # Plugs the text file's contents into a render template
    # for the given page
    with open("pages/" + page_name + ".txt", "r") as f:
        cc = f.read()
    return render_template("editform.html", current_contents=cc, page=page_name)


@app.route("/edit/", methods=["GET", "POST"])
def edit_page():
    # Receives content and changes information from server
    page_name = request.form["page_name"]
    con = request.form["contents"]
    # cha = request.form["changes"]

    # Variables for the text and html file path's for <page_name>
    fullpath = "pages/" + page_name + ".txt"
    template_path = page_name + ".html"

    con = filter_info(con)
    # Writes the changes to the text file
    with open(fullpath, "w") as f:
        f.write(Markup(con))

    # Returns the template with filtered data
    return render_template(template_path, contents=Markup(con))
