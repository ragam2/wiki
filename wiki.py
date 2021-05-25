from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello, World!\n"

@app.route(...)
def handle_request(...):
    # TODO: load the desired page content
    return render_template(
        "main",
        page_name=...,
        page_content=...,
    )

@app.route("/view/<pagename>")
def get_frontpage():
    # TODO: load the desired page content
    return render_template(
        "main",
        page_name=...,
        page_content=...,
    )

@app.route("/view/<pagename>")
def get_pagename(pagename):
    # TODO: load the desired page content
    return render_template(
        "main",
        page_name=...,
        page_content=...,
    )