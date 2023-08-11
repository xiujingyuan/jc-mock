from flask import Blueprint
api_quality_info = Blueprint('api_quality_info', __name__)

from . import quality_info_api