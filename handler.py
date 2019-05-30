import json
import re

import requests


def extract_title(event, context):

    if "queryStringParameters" not in event:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": "No query string is given",
        }

    if "url" not in event["queryStringParameters"]:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": "URL is not given",
        }

    # Get URL from the query string parameters
    url = event["queryStringParameters"]["url"]

    try:
        html = requests.get(url)

    except:
        body = {"message": "Please enter a valid URL"}
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body),
        }

    html = html.text

    title = find_title(html)

    if not title:
        body = {"message": "Title not found. Please check your URL."}
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body),
        }

    body = {"title": title}

    response = {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

    return response


def find_title(html):
    title_pattern = re.compile("((<title.*?>(.*?)</title>))", re.I | re.S)
    match = title_pattern.search(html)
    return match.group(3)
