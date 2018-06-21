import os

from dotenv import load_dotenv
from flask_env import MetaFlaskEnv

load_dotenv()


class Config(metaclass=MetaFlaskEnv):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DATABASE'),
        'username': os.environ.get('MONGO_USERNAME'),
        'password': os.environ.get('MONGO_PASSWORD'),
        'host': os.environ.get('MONGO_HOST')
    }
