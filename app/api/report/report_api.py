import json
from datetime import datetime
from app.api.report import api_report
from app import csrf
from flask import jsonify, request, current_app, Response, render_template
from sqlalchemy import and_
from app.models.TapdKeyValueDb import TapdKeyValue
from app.report.story_report_view import get_iterations


@api_report.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Case!'


@api_report.route('/get_iteration/<string:work_id>', methods=['GET'])
def get_work_iteration(work_id):
    """
    获取指定项目的迭代信息
    :param work_id: 项目的work_id
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed",
            "data": []
        }
        find_iterations = TapdKeyValue.query.filter(and_(TapdKeyValue.key == "tapd_info",
                                                         TapdKeyValue.type == "iteration",
                                                         TapdKeyValue.workspace_id == work_id)).first()
        if find_iterations:
            iterion = get_iterations(work_id, json.loads(find_iterations.value), {}, datetime.now().date())
            data["code"] = 0
            data["msg"] = "success"
            data["data"] = iterion[work_id]
        else:
            data["msg"] = "not found the iteraton!"

    except Exception as e:
        current_app.logger.exception(e)
        data["msg"] = str(e)
    return jsonify(data)
