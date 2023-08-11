from flask import Blueprint

view_upload = Blueprint('upload', __name__)

from . import upload_file