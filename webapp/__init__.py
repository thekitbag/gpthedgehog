from flask import Flask
from config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    cors = CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})

    from webapp.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
