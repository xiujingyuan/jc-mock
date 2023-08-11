
from flask import jsonify, request
from app.api.quality_info import api_quality_info
from app.models.QualityInfoDb import QualityInfo
from app import db


@api_quality_info.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Quality!'


@api_quality_info.route('/update/', methods=['POST'])
def update_quality_info():
    ret_data = {
        "code": 1,
        "data": "",
        "msg": "更新失败"
    }
    if "task_id" not in request.json:
        ret_data["msg"] = "task_id not found!"
    elif "story_change_count" not in request.json:
        ret_data["msg"] = "story_change_count not found!"
    elif "smoke_count" not in request.json:
        ret_data["msg"] = "smoke_count not found!"
    elif "reason" not in request.json:
        ret_data["msg"] = "reason not found!"
    elif "level" not in request.json:
        ret_data["msg"] = "level not found!"
    elif "operator" not in request.json:
        ret_data["msg"] = "operator not found!"
    else:
        task_id = request.json["task_id"]
        story_change_count = request.json["story_change_count"]
        smoke_count = request.json["smoke_count"]
        reason = request.json["reason"]
        level = request.json["level"]
        operator = request.json["operator"]
        find_quality_info = db.session.query(QualityInfo).filter(QualityInfo.task_id == task_id).first()
        if not find_quality_info:
            find_quality_info = QualityInfo()
            find_quality_info.task_id = task_id
        find_quality_info.reason = reason
        find_quality_info.operator = operator
        find_quality_info.story_change_count = story_change_count
        find_quality_info.smoke_count = smoke_count
        find_quality_info.level = level
        db.session.add(find_quality_info)
        db.session.flush()
        ret_data["code"] = 0
        ret_data["msg"] = '更新成功'
    return jsonify(ret_data)


@api_quality_info.route('/<int:build_task_id>', methods=['GET'])
def get_quality_info(build_task_id):
    ret_data = {
        "code": 0,
        "data": {
            "story_change_count": 0,
            "smoke_count": 0,
            "reason": "",
            "level": 0
        },
        "msg": "获取成功"
    }
    find_quality_info = QualityInfo.query.filter(QualityInfo.task_id == build_task_id).first()
    if find_quality_info:
        ret_data["data"]["story_change_count"] = find_quality_info.story_change_count
        ret_data["data"]["smoke_count"] = find_quality_info.smoke_count
        ret_data["data"]["reason"] = find_quality_info.reason
        ret_data["data"]["level"] = find_quality_info.level
    return jsonify(ret_data)
