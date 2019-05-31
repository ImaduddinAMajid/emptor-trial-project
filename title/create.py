import json
import os
import re

import boto3
import requests


BUCKET = os.environ["S3_BUCKET"]
KEY_BASE = os.environ["S3_KEY_BASE"]

s3_client = boto3.client("s3")


def create(event, context):
    data = json.loads(event["body"])

    body = {}

    if data is None:
        body["message"] = "No query string is given"
        return create_response(400, body)

    if "url" not in data:
        body["message"] = "URL is not given"
        return create_response(400, body)

    # Get URL from the request body
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

    # Store response body to S3 Bucket
    object_name = KEY_BASE + f"{title}.html"
    store_to_s3_bucket(html, BUCKET, object_name)

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


def store_to_s3_bucket(response_body, bucket, object_name=None):
    return s3_client.put_object(Body=response_body, Bucket=bucket, Key=object_name)
