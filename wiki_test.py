import pytest

import wiki


@pytest.fixture
def client():
    wiki.app.config["TESTING"] = True

    with wiki.app.test_client() as client:
        yield client


def test_import():
    assert wiki is not None

def test_front_page(client):
    resp = client.get("/view/", follow_redirects = True)
    assert resp.status_code == 200
    assert b"Hello, this is the Arch team's front page!" in resp.data

def test_page_name(client):
    resp = client.get("/view/PageName")
    print(resp.data)
    assert resp.status_code == 200
    assert b"Page Contents\nName\nText" in resp.data

    