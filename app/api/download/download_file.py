from flask import send_from_directory, current_app
from app.api.download import api_download
import os


@api_download.route('/<filepath>', methods=['GET'])
def download_file_func(filepath):
    print("filepath:", filepath)
    target_path = os.path.join(current_app.config["FILE_HOME"], current_app.config["DOWNLOAD_FOLDER"])
    return send_from_directory(target_path, filepath, as_attachment=True)

