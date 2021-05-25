import pytest

import wiki


@pytest.fixture
def client():
    wiki.app.config["TESTING"] = True

    with wiki.app.test_client() as client:
        yield client


def test_import():
    assert wiki is not None


def test_homepage(client):
    resp = client.get("/view/")
    print(resp.data)
    assert resp.status_code == 200
    assert b"<pre>Hello, this is the Arch team&#39;s front page!</pre>" in resp.data

def test_pagename(client):
    resp = client.get("/view/PageName")
    assert resp.status_code == 200
    assert b"<pre>Page Name Contents</pre>" in resp.data