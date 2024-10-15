from flask import Flask
from config import Config
from flask_cors import CORS
from .database import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from webapp.models import User


login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS'], "supports_credentials": True}})
    
    migrate = Migrate(db)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from webapp.main import bp as main_bp
    app.register_blueprint(main_bp)

    from webapp.account import bp as account_bp
    app.register_blueprint(account_bp)

    return app





