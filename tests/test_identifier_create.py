import json
import os


from identifier.create import create
from tests import *

context = {}


def test_identifier_create():
    body = {"url": "https://www.emptor.io"}
    response = create(api_gateway_event("POST", body=body), context)
    identifier = json.loads(response["body"])["identifier"]
    assert response["statusCode"] == 200
    assert type(identifier) == str