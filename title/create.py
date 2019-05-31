import json
import os
import re
import uuid

import boto3
import requests

from log_config import logger
from title.title_model import TitleModel, State
from utils import create_response


s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")


def create(event, context):
    logger.debug(f"event: {event}")

    BUCKET = os.environ["S3_BUCKET"]
    KEY_BASE = os.environ["S3_KEY_BASE"]

    body = {}

    if "identifier" not in event:
        body["message"] = "Request id not found"
        return create_response(400, body)

    request_id = event["identifier"]
    title_model = TitleModel.get(hash_key=request_id)

    # Get URL from DynamoDB record
    url = title_model.url

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

    # Store response body to S3 Bucket
    object_name = KEY_BASE + f"{title}.html"
    s3_url = store_to_s3_bucket(html, BUCKET, object_name)

    title_model.title = title
    title_model.s3_url = s3_url
    title_model.state = State.PROCESSED.name

    title_model.save()

    response = create_response(body=dict(title_model))

    return response


def find_title(html):
    title_pattern = re.compile("((<title.*?>(.*?)</title>))", re.I | re.S)
    match = title_pattern.search(html)
    return match.group(3)


def store_to_s3_bucket(response_body, bucket_name, object_name):
    s3_client.put_object(Body=response_body, Bucket=bucket_name, Key=object_name)
    url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
    return url
