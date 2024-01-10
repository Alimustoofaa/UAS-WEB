from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

SECRET_KEY = '4YrzfpQ4kGXjuP6wasdfKJwer*&6qwasd'

DB = {
    'host': 'sql12.freemysqlhosting.net:3306',
    'user': 'sql12675593',
    'pass': 'XTGCB4c96D',
    'name': 'sql12675593'
}

DB_URI = f'mysql+pymysql://{DB["user"]}:{DB["pass"]}@{DB["host"]}/{DB["name"]}?charset=utf8mb4'

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'sg.login'

import simplegram.routes as routes