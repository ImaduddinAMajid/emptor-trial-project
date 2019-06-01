import json
import os
import re
import uuid

import boto3
import requests

from title.title_model import TitleModel
from utils import create_response

function_name = os.environ['PROCESSING_LAMBDA']
lambda_client = boto3.client('lambda')

def create(event, context):
    identifier = uuid.uuid1().__str__()

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

    body = {"identifier": identifier}

    # Store title as DynamoDB record
    title_model = TitleModel()
    title_model.request_id = identifier
    title_model.url = url
    title_model.save()

    response = create_response(body=body)

    return response
