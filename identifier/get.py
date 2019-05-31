from log_config import logger
from title.title_model import TitleModel
from utils import create_response

def get(event, context):
    logger.debug(f'event: {event}')
    
    body = {}
    
    if "request_id" not in event["pathParameters"]:
        body["message"] = "Request id not found"
        return create_response(400, body)

    request_id = event['pathParameters']['request_id']
    title_model = TitleModel.get(hash_key=request_id)

    response = create_response(body=dict(title_model))

    return response
