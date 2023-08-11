from flask import Blueprint
api_report = Blueprint('api_report', __name__)

from . import report_api