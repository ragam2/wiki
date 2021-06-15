import pytest  # type: ignore
import wiki
from flask import Markup

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
    resp = client.get("/view/Game_of_Thrones", follow_redirects=True)
    with open("pages/Game_of_Thrones.txt", "r") as f:
        expected = bytes(f.read(), "utf-8")
    assert resp.status_code == 200
    assert expected in resp.data


def test_edit_form(client):
    # Tests if the submission form is sending data to correct location,
    # and if the correct page is present in the form.
    resp = client.get("/edit-form/Game_of_Thrones", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Game of Thrones" in resp.data
    assert b"/edit/" in resp.data


def test_edit_page(client):
    resp = client.get(
        "edit-form/Game_of_Thrones?page=Game_of_Thrones",
    )
    print(resp.data)
    assert resp.status_code == 200
    assert b"Page Edit" in resp.data
    assert b"Enter your changes" in resp.data


def test_filter_info():
    # For some reason, it seems you have to import filter_info and markup
    # individually rather than just from wiki.

    # This asserts that invalid text (<script>, etc) is escaped,
    # and valid text (h1, h2, h3, p, a) is not escaped
    # and no tags also go through

    assert wiki.filter_info("<h1>Hello World!</h1><p>Hello World!</p>") == (
        True,
        Markup("<h1>Hello World!</h1><p>Hello World!</p>"),
    )

    assert wiki.filter_info("Hello World!") == (True, Markup("Hello World!"))
