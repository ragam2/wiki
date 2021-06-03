import pytest

# from flask import Flask, redirect, url_for
# from flask import request, Markup
# from flask import render_template

import wiki

CURR_DIR = "pages"


@pytest.fixture
def client():
    wiki.app.config["TESTING"] = True

    with wiki.app.test_client() as client:
        yield client


def test_import():
    assert wiki is not None


def test_front_page(client, tmpdir):
    resp = client.get("/")
    with open("pages/main.txt", "r") as f:
        # bytes() is similar to making a byte string by using b"String"
        expected = bytes(f.read(), "utf-8")
    assert resp.status_code == 200
    assert expected in resp.data


def test_page_name(client):
    resp = client.get("/view/test_page", follow_redirects=True)
    with open("pages/test_page.txt", "r") as f:
        expected = bytes(f.read(), "utf-8")
    assert resp.status_code == 200
    assert expected in resp.data


def test_edit_form(client):
    # Tests if the submission form is sending data to correct location,
    # and if the correct page is present in the form.
    resp = client.get("/edit-form/test_page", follow_redirects=True)
    print(resp.data)
    assert resp.status_code == 200
    assert b"Hello World!" in resp.data
    assert b"/edit/" in resp.data
    assert b"test_page" in resp.data


def test_edit_page(client):
    resp = client.get(
        "/edit/",
        follow_redirects=True,
        data=dict(
            page_name="test_page",
            contents=("<h1>Hello World!</h1>" "<p>This the the first test page!</p>"),
            changes="greeting added",
        ),
    )
    print(resp.data)
    with open("pages/test_page.txt", "r") as f:
        expected = bytes(f.read(), "utf-8")
    assert resp.status_code == 200
    assert expected in resp.data
