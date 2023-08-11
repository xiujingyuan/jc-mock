from flask import Blueprint

api_download = Blueprint('download', __name__)

from . import download_file
