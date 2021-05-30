import pytest

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
    resp = client.get("/view/", follow_redirects = True)
    print(resp.data)
    assert resp.status_code == 200
    assert b"Welcome to Arch's Frontpage!" in resp.data

def test_page_name(client):
    resp = client.get("/view/PageName")
    print(resp.data)
    assert resp.status_code == 200
    assert b"<h1> Title </h1>" in resp.data

def test_edit_form(client):
    resp = client.get("/view/handle-page-edits")
    assert resp.status_code == 200

    