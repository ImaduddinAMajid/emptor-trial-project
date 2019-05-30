import json

from handler import extract_title
from tests import *

context = {}


def test_handler_extract_title():
    query = {"url": "https://www.emptor.io"}
    response = extract_title(
        api_gateway_event("POST", query_string_parameters=query), context
    )
    title = json.loads(response["body"])["title"]
    assert response["statusCode"] == 200
    assert title == "Emptor- Home page"
