import redis
import json
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup Redis
REDIS_HOST = os.getenv('REDIS_HOST', '192.168.1.231')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
# redis_url = os.getenv('REDIS_URL', 'redis://admin:Huawei%4012345!@192.168.1.29:6379/0')
# redis_client = redis.StrictRedis.from_url(redis_url)

def push_to_redis(result):
    result_id = result['result_id']
    redis_client.set(result_id, json.dumps(result), ex=3600) # Cache for 1hour

def fetch_from_redis(result_id):
    result = redis_client.get(result_id)
    if result:
        return json.loads(result)
    return None

