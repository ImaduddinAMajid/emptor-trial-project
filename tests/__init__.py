import json


def api_gateway_event(method="GET", body=None, query_string_parameters=None):
    return {
        "body": json.dumps(body) if body else None,
        "method": method,
        "principalId": "",
        "stage": "dev",
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-us",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Cookie": "__gads=ID=d51d609e5753330d:T=1443694116:S=ALNI_MbjWKzLwdEpWZ5wR5WXRI2dtjIpHw; __qca=P0-179798513-1443694132017; _ga=GA1.2.344061584.1441769647",
            "Host": "xxx.execute-api.us-east-1.amazonaws.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
            "Via": "1.1 c8a5bb0e20655459eaam174e5c41443b.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "z7Ds7oXaY8hgUn7lcedZjoIoxyvnzF6ycVzBdQmhn3QnOPEjJz4BrQ==",
            "X-Forwarded-For": "221.24.103.21, 54.242.148.216",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "query": {},
        "queryStringParameters": query_string_parameters,
        "path": {},
        "identity": {
            "cognitoIdentityPoolId": "",
            "accountId": "",
            "cognitoIdentityId": "",
            "caller": "",
            "apiKey": "",
            "sourceIp": "221.24.103.21",
            "cognitoAuthenticationType": "",
            "cognitoAuthenticationProvider": "",
            "userArn": "",
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
            "user": "",
        },
        "stageVariables": {},
    }


def s3_object_created_event(bucket_name, key):
    return {
        "Records": [{"s3": {"object": {"key": key}, "bucket": {"name": bucket_name}}}]
    }


def lambda_invoke_event(body):
    return body


def dynamodb_stream_event(body):
    return {
        "Records": [
            {
                "eventID": "7c948c6b4f6b8015b5f6a7e027ad2604",
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "eu-central-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1559376924.0,
                    "Keys": {"request_id": {"S": body["identifier"]}},
                    "SequenceNumber": "100000000007020339446",
                    "SizeBytes": 46,
                    "StreamViewType": "KEYS_ONLY",
                },
                "eventSourceARN": "arn:aws:dynamodb:eu-central-1:027224929341:table/emptor-docs-processing-prod/stream/2019-06-01T08:12:06.020",
            }
        ]
    }
