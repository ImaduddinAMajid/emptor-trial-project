import json
import os

import boto3
from botocore.exceptions import ClientError
from moto import mock_s3
import pytest
import requests

from title.create import create, find_title, KEY_BASE
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

    body = {"url": ""}
    response = create(api_gateway_event("POST", body=body), context)
    message = json.loads(response["body"])["message"]
    assert response["statusCode"] == 400
    assert message == "Please enter a valid URL"


def test_title_create_store_s3():
    """
    Please export ENVIRONMENT VARIABLES in your environment replicating
    AWS Lambda environment variables. See serverless.yml for configured
    environment variables.
    """
    with mock_s3():
        conn = boto3.resource("s3", region_name="us-east-1")
        if not conn.Bucket("emptor-test-bucket") in conn.buckets.all():
            conn.create_bucket(ACL="public-read-write", Bucket="emptor-test-bucket")
    os.environ["S3_BUCKET"] = "emptor-test-bucket"
    body = {"url": "https://www.emptor.io"}
    response = create(api_gateway_event("POST", body=body), context)
    title = json.loads(response["body"])["title"]
    object_name = KEY_BASE + f"{title}.html"
    obj = conn.Object("emptor-test-bucket", object_name).get()
    assert (
        find_title(
            str(conn.Object("emptor-test-bucket", object_name).get()["Body"].read())
        )
        == title
    )
