import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    dbhost = os.getenv('DBHOST')
    dbuser = os.getenv('DBUSER')
    dbpass = os.getenv('DBPASS')
    port = os.getenv('PORT')
    dbname = os.getenv('DBNAME')

