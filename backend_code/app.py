from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import cv2
import numpy as np
import os
import logging
from obs_func import *
from database import *
from redis_operations import *
import requests
from push_to_obs_fg import *
from obs_func import obs_push_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load the model
try:
    retina_face_detection = pipeline(Tasks.face_detection, 'damo/cv_resnet50_face-detection_retinaface')
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")

SHARED_DIRECTORY = os.getenv('SHARED_DIRECTORY', '/test')
UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', 'uploaded_images')
OUTPUT_DIRECTORY = os.getenv('OUTPUT_DIRECTORY', 'output')
os.makedirs(os.path.join(SHARED_DIRECTORY, UPLOAD_DIRECTORY), exist_ok=True)
os.makedirs(os.path.join(SHARED_DIRECTORY, OUTPUT_DIRECTORY), exist_ok=True)

# APIG's url
URL = os.getenv('URL', 'https://6e123eded88f4fc5b801d30c676805c2.apig.ap-southeast-3.huaweicloudapis.com/push-to-obs')

@app.route('/predict', methods=['POST'])
def predict():
    logger.debug("Before Try")
    logger.debug(f'File name: {request.files["image"].filename}')
    try:
        logger.info("Inside predict function")
        if 'image' not in request.files:
            logger.error("No image file provided.")
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        image_path = os.path.join(SHARED_DIRECTORY, UPLOAD_DIRECTORY, image_file.filename)
        image_file.save(image_path)
        logger.info("Image uploaded successfully.")

        # Push original image to OBS with Function Graph APIG
        resp = push_to_obs(image_path, URL, image_file.filename)
        print(resp.status_code, resp.reason)
        print(resp.content)
        logger.info("Successfully push original image to OBS")

        # Push original image to OBS
        # resp = obs_push_file(image_file.filename, image_path)
        # print(resp.status_code, resp.reason)
        # print(resp.content)
        # logger.info("Successfully push original image to OBS")

        # Check Redis for existing result
        cached_result = fetch_from_redis(image_file.filename)
        if cached_result:
            logger.info("Cache hit - returning cached result")
            return jsonify(cached_result)

        # Perform model inference
        result = retina_face_detection(image_path)
        logger.debug(f"Detection result: {result}")

        if 'boxes' not in result or 'keypoints' not in result:
            logger.error("Invalid detection result.")
            return jsonify({'error': 'Invalid detection result'}), 500

        image = cv2.imread(image_path)
        if image is None:
            logger.error("Failed to read uploaded image.")
            return jsonify({'error': 'Failed to read uploaded image'}), 500
        
        image = draw_image(image, result)

        output_path = os.path.join(SHARED_DIRECTORY, OUTPUT_DIRECTORY, f'output_{image_file.filename}')
        success = cv2.imwrite(output_path, image)
        logger.info("Output image saved successfully.")
        if success:
            logger.info("Output image saved successfully at %s", output_path)
        else:
            logger.error("Failed to save output image at %s", output_path)
            return jsonify({'error': 'Failed to save output image'}), 500

        # Push result to OBS with Function Graph APIG
        resp = push_to_obs(output_path, URL, f'output_{image_file.filename}')
        print(resp.status_code, resp.reason)
        print(resp.content)
        logger.info("Successfully push output image to OBS")

        # Push original image to OBS
        # resp = obs_push_file(f'output_{image_file.filename}', output_path)
        # print(resp.status_code, resp.reason)
        # print(resp.content)
        # logger.info("Successfully push original image to OBS")

        # Prepare result for Redis
        redis_result = {
                'result_id': image_file.filename,
                'result': result,
                'output_image': f'/images/output_{image_file.filename}'
        }
        # Push result to Redis
        push_to_redis(redis_result)
        logger.info("Successfully pushed to Redis")

        # Push result to database
        push_result_to_db(
            boxes=str(result['boxes']),
            keypoints=str(result['keypoints'])
        )

        return jsonify({
            'result': result,
            'output_image': f'/images/output_{image_file.filename}'
        })
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/images/<filename>')
def get_image(filename):
    """if os.path.exists(os.path.join(OUTPUT_DIRECTORY, filename)):
        logger.info("File exist.")
        response = make_response(send_from_directory(OUTPUT_DIRECTORY, filename))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        logger.error("File doesn't exist.")
        return "File not found", 404
    """
    try:
        image_path = os.path.join(SHARED_DIRECTORY, OUTPUT_DIRECTORY, filename)
        logger.info(f"Attempting to serve image: {image_path}")
        if os.path.exists(image_path):
            logger.info(f"Serving image: {filename}")
            return send_from_directory(os.path.join(SHARED_DIRECTORY, OUTPUT_DIRECTORY), filename)
        else:
            logger.error(f"File {filename} doesn't exist at path {image_path}")
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error serving image: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# Image proccess with result
def draw_image(image, result):
    for box in result['boxes']:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2) # Blue color, thickness of 2

    for keypoints in result['keypoints']:
        for i in range(0, len(keypoints), 2):
            x, y = int(keypoints[i]), int(keypoints[i+1])
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1) # Red color, filled with circle

    return image

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

