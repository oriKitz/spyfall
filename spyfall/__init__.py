from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config


app = Flask(__name__)
# app.config.from_object('Config')
app.config['SECRET_KEY'] = '9ed456ae10f7eb034612afd2a46790bf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['LOCATIONS'] = ['Hospital', 'Airplane', 'Police Station', 'Circus Tent']
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)

from spyfall import views
