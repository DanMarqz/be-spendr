import os
from dotenv import load_dotenv
load_dotenv(override=True)

APP_SECRET_KEY  = os.getenv('APP_SECRET_KEY')
VERSION         = os.getenv('VERSION')
PORT            = os.getenv('PORT')
TOKEN           = os.getenv('TOKEN')
DB_URI          = os.getenv('DB_URI')
DB_NAME         = os.getenv('DB_NAME')

def loaded():
    print("Variables loaded...")