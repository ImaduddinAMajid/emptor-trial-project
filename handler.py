import json


def extract_title(event, context):

    if 'queryStringParameters' not in event:
        return {'statusCode': 400,
        'headers': {'Content-Type': 'application/json'},
        'body': 'No query string is given'}

    if 'url' not in event['queryStringParameters']:
        return {'statusCode': 400,
        'headers': {'Content-Type': 'application/json'},
        'body': 'URL is not given'}

    url = event['queryStringParameters']['url']

    body = {
        "message": f"Input URL: {url}",
        "input": event
    }

    response = {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }

    return response
