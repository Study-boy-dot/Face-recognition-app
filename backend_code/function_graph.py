# -*- coding:utf-8 -*-
import json
from obs_func import obs_push_file
import base64
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handler (event, context):
    # Get the input data
    img_info = event['body']

    # Data will be encoded in b64 type, need to decode first
    decode_img_info = base64.b64decode(img_info)

    # Turn binary type to string
    str_img_info = decode_img_info.decode('utf-8')

    # Turn string to dictionary
    dict_img_info = json.loads(str_img_info)

    # Get the image data
    img_data = base64.b64decode(dict_img_info['img'])
    with open(f'/tmp/{dict_img_info["file name"]}', 'wb') as file:
        file.write(img_data)
        logger.info('Successfully write temp image data')

    # Push file to OBS
    obs_push_file(dict_img_info['file name'], f'/tmp/{dict_img_info["file name"]}')
    logger.info("Push file to OBS successfully")
    
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(event),
        "headers": {
            "Content-Type": "application/json"
        }
    }