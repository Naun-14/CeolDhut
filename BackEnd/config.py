import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(BASE_DIR, "routes", ".env"))


def clean_env(name, default=None):
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else value


DATABASE_URL = clean_env('DATABASE_URL', 'mysql+pymysql://root:january07W@localhost/ceoldhut')
SECRET_KEY = clean_env('SECRET_KEY', 'ceoldhut key')
ENGINE_OPTIONS = {}

if DATABASE_URL.startswith('mysql+pymysql://') and 'aivencloud.com' in DATABASE_URL:
    ENGINE_OPTIONS = {
        'connect_args': {
            'ssl': {}
        }
    }


class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = ENGINE_OPTIONS
    SECRET_KEY = SECRET_KEY
