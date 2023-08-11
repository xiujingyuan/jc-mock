import os
import platform
import traceback

from flask import request, current_app, redirect, flash
from werkzeug.utils import secure_filename
import codecs
from app.api.upload import view_upload
from flask import jsonify
from app import db
from app.common.xmind_to_testcase import xmind_to_tapd_excel_file
from app.models.AssumptBuildTaskDb import AssumptBuildTask

ALLOW_EXTENSIONS = set(['xmind'])


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


@view_upload.route('/<string:file_name>/<string:story_id>/<string:task_index>', methods=['POST'])
def upload_file(file_name, story_id, task_index):
    # check if the post request has the file part
    try:
        xml_file = request.files['file']
        if xml_file.filename == '':
            return jsonify({"code": 1, 'message': 'filename is null'})
        if xml_file and allowed_file(xml_file.filename):

            file_path = os.path.join(current_app.config["FILE_HOME"], current_app.config['UPLOAD_FOLDER'], file_name)
            xml_file.save(file_path)
            tapd_xls_file = xmind_to_tapd_excel_file(file_path)
            tapd_xls_name = os.path.basename(tapd_xls_file)
            tapd_xls_file_new = os.path.join(current_app.config["FILE_HOME"],
                                             current_app.config['DOWNLOAD_FOLDER'],
                                             tapd_xls_name)
            tapd_xls_file_url = os.path.join("/api/download/", tapd_xls_name)
            os.rename(tapd_xls_file, tapd_xls_file_new)
            get_task = AssumptBuildTask.query.filter(AssumptBuildTask.story_id == story_id).first()
            if get_task:
                get_task.case_name = tapd_xls_file_url
                db.session.add(get_task)
                db.session.flush()
            return jsonify({"code": 0, 'message': "上传完成", "file_name": tapd_xls_file_url, "index": task_index})
    except:
        return jsonify({"code": 1, 'message': traceback.format_exc()})

