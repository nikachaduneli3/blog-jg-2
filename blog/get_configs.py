from dotenv import load_dotenv
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

DEBUG = os.getenv('DEBUG', "False")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT=os.getenv('EMAIL_PORT')
EMAIL_HOST_USER=os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS=os.getenv('EMAIL_USE_TLS')
SECRET_KEY=os.getenv('SECRET_KEY')
DB_ENGINE=os.getenv('DB_ENGINE')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')

def get_db_conf():
    if DEBUG == 'False':
        return {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            }
        }
    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
print(get_db_conf())
