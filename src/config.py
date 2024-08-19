import os

API_TOKEN = "your_static_token"

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

DATA_DIRECTORY = os.getcwd() + "/data"
DATA_IMAGE_DIRETORY = os.getcwd() + "/data/images"
BASE_URL = "https://dentalstall.com/shop/"