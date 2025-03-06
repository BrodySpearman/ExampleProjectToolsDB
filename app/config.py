import os
from dotenv import load_dotenv

# Load environment variables from .env file in statelineDB/app/db_info.env
load_dotenv(r'app\db_info.env')

class Config(object):
    DBHOST = os.getenv('DBHOST')
    DBUSER = os.getenv('DBUSER')
    DBPASS = os.getenv('DBPASS')
    DBNAME = os.getenv('DBNAME')
    DBURL = os.getenv('DB_URL')

