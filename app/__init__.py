from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.create_all(app=app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .routes import main as main_blueprint
app.register_blueprint(main_blueprint)

from .appfuncs import add_standart_values
add_standart_values()
