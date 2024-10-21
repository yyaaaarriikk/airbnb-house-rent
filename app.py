from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

db.init_app(app)
login_manager.init_app(app)

from routes import *
from models import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)