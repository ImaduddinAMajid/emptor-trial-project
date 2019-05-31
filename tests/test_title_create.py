import json
import os

import boto3
from botocore.exceptions import ClientError
from moto import mock_s3
import pytest
import requests

from title.create import create, find_title, store_to_s3_bucket
from tests import *

context = {}
BUCKET = os.environ["S3_BUCKET"]
KEY_BASE = os.environ["S3_KEY_BASE"]


def test_title_create():
    os.environ["S3_BUCKET"] = "emptor-body-response"
    body = {"url": "https://www.emptor.io"}
    response = create(api_gateway_event("POST", body=body), context)
    response_body = json.loads(response["body"])
    title = response_body["title"]
    s3_url = response_body["s3URL"]
    assert response["statusCode"] == 200
    assert (
        s3_url
        == "https://emptor-body-response.s3.amazonaws.com/testEmptor- Home page.html"
    )
    assert title == "Emptor- Home page"


def test_title_create_null_body():
    response = create(api_gateway_event("POST"), context)
    message = json.loads(response["body"])["message"]
    assert response["statusCode"] == 400
    assert message == "Request body not found"


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


def test_store_to_s3_bucket():
    bucket_name, object_name = "emptor-test-bucket", "test-store-s3.txt"
    with mock_s3():
        conn = boto3.resource("s3", region_name="us-east-1")
        if not conn.Bucket(bucket_name) in conn.buckets.all():
            conn.create_bucket(ACL="public-read-write", Bucket=bucket_name)
        body = "storing test"
        store_to_s3_bucket(body, bucket_name, object_name)
        obj = conn.Object(bucket_name, object_name).get()["Body"]
        assert obj.read() == bytes(body, "utf-8")
