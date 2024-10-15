from flask import Blueprint

bp = Blueprint('account', __name__, url_prefix='/api')

from webapp.account import routes