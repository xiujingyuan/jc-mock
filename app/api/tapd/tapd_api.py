#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/18
 @file: system_api.py
 @site:
 @email:
"""
import datetime
import json
import traceback

from flask_login import current_user
from app import csrf, db
from app.api.tapd import api_tapd
from flask import request, current_app
from flask import jsonify
from sqlalchemy import and_
from app.api.tapd.publish_email_demo import get_publish_email_content
from app.common.Tapd import get_tapd_api, post_tapd_api, get_tapd_story, get_special_status_story_completed_time
from app.common.send_email.mail_receive import mail_send
from app.models.AssumptBuildTaskLogDb import AssumptBuildTaskLog
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.AssumptEmailDb import AssumptEmail
from app.models.JenkinsJobDb import JenkinsJob
from app.common.Coverage import get_branch_commit, get_tag_commit
import requests

from app.models.KeyValueDb import KeyValue
from app.models.TapdKeyValueDb import TapdKeyValue
from app.models.TapdStoryDetailDb import TapdStoryDetail
from app.tools.tools import send_tv


@api_tapd.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Tapd!'


@api_tapd.route('/publish_story', methods=['POST'])
def publish_story():
    req = request.json
    ret = {
        "code": 1,
        "message": "",
        "data": []
    }
    try:
        if "build_task_id" not in req:
            ret["message"] = "not found the build_task_id"
        elif "user_name" not in req:
            ret["message"] = "not found the user_name"
        else:
            assumpt_task = db.session.query(AssumptBuildTask).filter(AssumptBuildTask.id == req["build_task_id"]).first()
            if assumpt_task is None:
                ret["message"] = "The build task not found!"
            else:
                tapd_ret = get_tapd_api("stories/?workspace_id={0}&&id={1}".format(assumpt_task.work_id,
                                                                                   assumpt_task.story_full_id))
                try:
                    status = tapd_ret['data']['Story']['status']
                except:
                    status = "not found"
                # 记录日志
                assumpt_log = AssumptBuildTaskLog()
                assumpt_log.build_task_id = req["build_task_id"]
                assumpt_log.person = req["user_name"]
                assumpt_log.modify_content_old = json.dumps({"status": status})
                assumpt_log.modify_content = json.dumps({"status": "resolved"})

                db.session.add(assumpt_log)
                db.session.flush()
                #
                # map_status = get_tapd_api("workflows/status_map?system=story&workspace_id={0}".format(
                #     assumpt_email.work_id))["data"]
                post_ret = publist_tapd_story(assumpt_task.work_id, assumpt_task.story_full_id)

                get_publish_story = AssumptBuildTask.query.filter(and_(
                    AssumptBuildTask.story_full_id == assumpt_task.story_full_id,
                    AssumptBuildTask.publish_time)).first()

                story_info = post_ret["data"]["Story"]
                assumpt_task.build_task_status = 0
                assumpt_task.publish_time = datetime.datetime.now()

                db.session.add(assumpt_task)
                db.session.flush()
                # 发送上线邮件
                iteration_url = f"https://www.tapd.cn/{assumpt_task.work_id}/prong/" \
                                f"iterations/view/{assumpt_task.iteration_id}"
                get_iteration_info = TapdKeyValue.query.filter(and_(TapdKeyValue.key == "tapd_info",
                                                                    TapdKeyValue.type == "iteration",
                                                                    TapdKeyValue.workspace_id == assumpt_task.work_id)
                                                               ).first()
                iteration_name = "not found"
                if get_iteration_info and get_iteration_info.value:
                    for iter in json.loads(get_iteration_info.value):
                        if assumpt_task.iteration_id == iter["id"]:
                            iteration_name = iter["name"]
                            break

                if not get_publish_story:
                    subject = f"【{assumpt_task.program_name}】{assumpt_task.story_name}-上线完成"
                    content = get_publish_email_content(assumpt_task.program_name,
                                                        assumpt_task.story_name,
                                                        assumpt_task.story_url,
                                                        req["user_name"],
                                                        iteration_name,
                                                        iteration_url,
                                                        assumpt_task.create_at,
                                                        assumpt_task.publish_time,
                                                        story_info["developer"][:-1] if story_info["developer"]
                                                        else story_info["developer"],
                                                        story_info["created"] if story_info is not None else "not found",
                                                        story_info["custom_field_99"][:-1] if story_info["custom_field_99"]
                                                        else story_info["custom_field_99"]
                                                        )
                    recipients = ["yangxuechao@kuainiugroup.com"]
                    cc = ["zhushasha@kuainiugroup.com"]
                    get_config_info = KeyValue.query.filter(KeyValue.key == "publish_email_recipients").first()
                    if get_config_info and get_config_info.value:
                        config_info = json.loads(get_config_info.value)
                        if str(assumpt_task.program_id) in config_info:
                            recipients = config_info[str(assumpt_task.program_id)]["recipients"]
                            cc = config_info[str(assumpt_task.program_id)]["cc"]
                    mail_send(subject, content, recipients, cc=cc)

                ret["code"] = 0
                ret["message"] = "success"

                # 调用jacoco关闭接口
                build_jenkins_job = assumpt_task.build_jenkins_jobs if assumpt_task.build_jenkins_jobs else None
                if build_jenkins_job is not None:
                    jenkins_job_list = JenkinsJob.query.filter(
                        JenkinsJob.gitlab_program_id == assumpt_task.gitlab_program_id).all()
                    for jenkins_job in jenkins_job_list:
                        super_jacoco_data = {
                            "uuid": jenkins_job.service_name + "_" + assumpt_task.build_branch,
                        }
                        requests.post(current_app.config["JENKINS_DICT"][jenkins_job.jenkins_url]["SUPER_JACOCO"] +
                                      current_app.config["SUPER_JACOCO_STOP"], json=super_jacoco_data)
    except Exception as e:
        send_tv("发布需求报错：%s" % str(e))
        send_tv("发布需求报错：%s" % str(traceback.format_exc()))
    return jsonify(ret)


@api_tapd.route('/fix_story_status', methods=['POST'])
def fix_story_status():
    ret = {
        "code": 1,
        "message": "",
        "data": []
    }
    args = request.json
    created_date = args['created_date']
    work_id = args['work_id']
    stories = get_tapd_story(work_id, query_start_time=created_date)
    for story in stories:
        story_id = story["Story"]["id"]
        search_story = db.session.query(TapdStoryDetail).filter(
            TapdStoryDetail.story_id == story_id).first()
        search_story.story_name = story["Story"]["name"]
        search_story.story_iteration_id = story["Story"]["iteration_id"]
        search_story.story_completed = story["Story"]["completed"]
        search_story.story_status = story["Story"]["status"]
        search_story.is_effective = 1
        if story["Story"]["status"] == "status_1":
            search_story.story_completed = get_special_status_story_completed_time(work_id, story["Story"]["id"])
        db.session.add(search_story)
    db.session.flush()
    ret["code"] = 0
    ret["message"] = "success"
    return jsonify(ret)


def publist_tapd_story(work_id, story_full_id):
    url = "stories"
    publish_status = "resolved"
    if work_id == "20352271":
        publish_status = "status_3"
    elif work_id == "58762743":
        publish_status = "status_2"
    elif work_id == "20272381":
        publish_status = "status_1"
    data = {
        "id": story_full_id,
        "status": publish_status,
        "workspace_id": work_id,
        "current_user": "test_platform",
        "completed": str(datetime.datetime.now())
    }
    post_ret = post_tapd_api(url, data)
    return post_ret


if __name__ == "__main__":
    publist_tapd_story("20262951", "1120262951001040212")
