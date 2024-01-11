import os
from dotenv import load_dotenv

load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

SECRET_KEY = os.getenv('SECRET_KEY')

DB = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'pass': os.getenv('DB_PASS'),
    'name': os.getenv('DB_NAME')
}

DB_URI = f'mysql+pymysql://{DB["user"]}:{DB["pass"]}@{DB["host"]}/{DB["name"]}?charset=utf8mb4'

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'sg.login'

import simplegram.routes as routes