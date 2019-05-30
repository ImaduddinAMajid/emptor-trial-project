import json

from title.create import create
from tests import *

context = {}


def test_title_create():
    body = {"url": "https://www.emptor.io"}
    response = create(api_gateway_event("POST", body=body), context)
    title = json.loads(response["body"])["title"]
    assert response["statusCode"] == 200
    assert title == "Emptor- Home page"


def test_title_create_invalid_url():
    body = {"url": "https://www.emptor"}
    response = create(api_gateway_event("POST", body=body), context)
    message = json.loads(response["body"])["message"]
    assert response["statusCode"] == 400
    assert message == "Please enter a valid URL"
