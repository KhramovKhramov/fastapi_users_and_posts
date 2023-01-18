from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_DB_NAME = os.environ.get('SQLITE_DB_NAME')
DB_URL = os.environ.get('DB_URL')