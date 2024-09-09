import logging
import os
from obs import ObsClient
from obs import PutObjectHeader
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Set OBS enviroment
OBS_ACCESS_KEY = os.getenv('OBS_ACCESS_KEY', 'default_access_key')
OBS_SECRET_KEY = os.getenv('OBS_SECRET_KEY', 'default_secret_key')
OBS_SERVER = os.getenv('OBS_SERVER', 'https://obs.ap-southeast-3.myhuaweicloud.com/')
OBS_BUCKET_NAME = os.getenv('OBS_BUCKET_NAME', 'model-inference')

obsClient = ObsClient(access_key_id=OBS_ACCESS_KEY,
                secret_access_key=OBS_SECRET_KEY,
                server=OBS_SERVER)
logger.info("OBS enviroment set successfully.")

OBJECT_OUTPUT_DIRECTORY = '/output'

def obs_push_file(object_name, file_path):
    # Push to OBS
    headers = PutObjectHeader()
    object_path = os.path.join(OBJECT_OUTPUT_DIRECTORY, object_name)
    resp = obsClient.putFile(OBS_BUCKET_NAME, object_path, file_path, headers)

    if resp.status < 300:
        print('Put File Succeeded')
        print('requestId:', resp.requestId)
        print('etag:', resp.body.etag)
        print('versionId:', resp.body.versionId)
        print('storageClass:', resp.body.storageClass)
        logger.info('Put File Succeeded')
    else:
        print('Put File Failed')
        print('requestId:', resp.requestId)
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
        logger.error('Put File Failed')

    return resp