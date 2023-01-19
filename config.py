from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_DB_NAME = os.environ.get('SQLITE_DB_NAME')
DB_URL = os.environ.get('DB_URL')
SECRET = os.environ.get('SECRET')
SECRET_KEY = os.environ.get('SECRET_KEY')