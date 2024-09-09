import requests
import json
import base64

def push_to_obs(file_path, url, file_name, auth=None):

    # Read the image file as bytes
    with open(file_path, mode="rb") as file:
        img = file.read()
    encoded_img = base64.b64encode(img).decode('utf-8')

    # url = 'http://9b6ec936945e4d9b8901ee1e6b5b6db2.apig.ap-southeast-1.huaweicloudapis.com/upload-to-obs'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'img': encoded_img,  # Replace with your request body as needed
        'file name': file_name
    }

    response = requests.post(url, headers=headers, json=data)
    return response
