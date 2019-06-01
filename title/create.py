from datetime import datetime
import json
import os
import re
import uuid

import boto3
import requests
from pynamodb.exceptions import DoesNotExist

from log_config import logger
from title.title_model import TitleModel, State
from utils import create_response


s3_client = boto3.client("s3")


def create(event, context):
    logger.debug(f"event: {event}")

    BUCKET = os.environ["S3_BUCKET"]
    KEY_BASE = os.environ["S3_KEY_BASE"]

    body = {}

    request_id = event["Records"][0]["dynamodb"]["Keys"]["request_id"]["S"]

    try:
        title_model = TitleModel.get(hash_key=request_id)
    except DoesNotExist:
        body = {"message": "Record not found"}
        logger.error(f"{body['message']}")
        return create_response(404, body)

    if title_model.state == State.PROCESSED.name:
        body = {"message": "Record is already processed."}
        logger.error(f"{body['message']}")
        return create_response(body)

    # Get URL from DynamoDB record
    url = title_model.url

    try:
        html = requests.get(url)
    except:
        body = {"message": "Please enter a valid URL"}
        logger.error(f"{body['message']}")
        return create_response(400, body)

    html = html.text

    title = find_title(html)

    if not title:
        body = {"message": "Title not found. Please check your URL."}
        logger.error(f"{body['message']}")
        return create_response(400, body)

    # Store response body to S3 Bucket
    object_name = KEY_BASE + f"{title}.html"
    s3_url = store_to_s3_bucket(html, BUCKET, object_name)

    title_model.update(
        attributes={
            "title": {"value": title, "action": "PUT"},
            "s3_url": {"value": s3_url, "action": "PUT"},
            "state": {"value": State.PROCESSED.name, "action": "PUT"},
            "updatedAt": {"value": datetime.now().astimezone(), "action": "PUT"},
        }
    )

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
