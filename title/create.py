import json
import os
import re
import uuid

import boto3
import requests

from title.title_model import TitleModel


s3_client = boto3.client("s3")


def create(event, context):
    BUCKET = os.environ["S3_BUCKET"]
    KEY_BASE = os.environ["S3_KEY_BASE"]

    body = {}

    if not event["body"]:
        body["message"] = "Request body not found"
        return create_response(400, body)

    data = json.loads(event["body"])

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

    # Store response body to S3 Bucket
    object_name = KEY_BASE + f"{title}.html"
    body["s3URL"] = store_to_s3_bucket(html, BUCKET, object_name)

    # Store title as DynamoDB record
    title_model = TitleModel()
    title_model.title_id = uuid.uuid1().__str__()
    title_model.title = title
    title_model.save()


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


def store_to_s3_bucket(response_body, bucket_name, object_name):
    s3_client.put_object(Body=response_body, Bucket=bucket_name, Key=object_name)
    url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    return url
