from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/api')

from webapp.main import routes