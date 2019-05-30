import json
import re

import requests


def create(event, context):
    data = json.loads(event["body"])

    body = {}

    if data is None:
        body["message"] = "No query string is given"
        return create_response(400, body)

    if "url" not in data:
        body["message"] = "URL is not given"
        return create_response(400, body)

    # Get URL from the query string parameters
    url = data["url"]

    try:
        html = requests.get(url)

    except:
        body = {"message": "Please enter a valid URL"}
        return create_response(400, body)

    html = html.text

    title = find_title(html)

    if not title:
        body = {"message": "Title not found. Please check your URL."}
        return create_response(400, body)

    body = {"title": title}

    response = create_response(body=body)

    return response


def find_title(html):
    title_pattern = re.compile("((<title.*?>(.*?)</title>))", re.I | re.S)
    match = title_pattern.search(html)
    return match.group(3)


def create_response(status_code=200, body=None):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
