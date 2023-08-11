from flask import Blueprint

ci_url = Blueprint('ci', __name__)

from . import ci_api