#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/15
 @file: task_api.py
 @site:
 @email:
"""
import html
import time
import traceback

import requests
from sqlalchemy import and_

from app import db
from app.api.coverage import api_coverage
from flask import request, jsonify, current_app

from app.common.Coverage import get_branch_commit_all, get_tag_commit, change_content
from app.common.Coverage import get_branch_commit as get_merge_branch_commit
from app.models.CoverageInfoDb import CoverageInfo
from app.models.JenkinsJobDb import JenkinsJob
from app.models.AssumptBuildTaskDb import AssumptBuildTask

from app.common.Coverage import get_branch_commit

import json
from app.tasks.coverage_task.coverage_task import CONTENT_DEFAULT


@api_coverage.route('/content', methods=['POST'])
def get_content():
    req = request.json
    ret = {
        "code": 1,
        "message": "获取源文失败",
        "data": []
    }
    if "url" not in req:
        ret['message'] = "url参数未找到"
    elif "lines" not in req:
        ret['message'] = "lines参数未找到"
    elif "addLines" not in req:
        ret['message'] = "addLines参数未找到"
    elif "filterLines" not in req:
        ret['message'] = "filterLines参数未找到"
    elif "system" not in req:
        ret['message'] = "system参数未找到"
    elif "branch" not in req:
        ret['message'] = "branch参数未找到"
    else:
        if req["url"].startswith("base/"):
            req["url"] = req["url"][5:]
        git_info = JenkinsJob.query.filter(JenkinsJob.service_name == req["system"]).first()

        if git_info is not None:
            file_url = current_app.config["JENKINS_DICT"][git_info.jenkins_url]["JACOCO_FILE"] + \
                       "/{1}_k8s_jacoco/{2}/{0}".format(req["url"], req['system'], req['branch'])
            get_file = requests.get(file_url)
            get_file.encoding = "utf-8"

            content = ""
            for index, line in enumerate(get_file.text.split("\n")):
                line = html.escape(line)
                line_str = '<span class="{0}"><i class="number_line">{1}.|</i>{2}</span><br >'
                class_style = ""
                if index in req['lines']:
                    class_style += "add_miss_line"
                if index in req["filterLines"]:
                    class_style += " add_filter_line"
                    if not req["lines"] or index not in req["lines"]:
                        class_style += " add_filter_coverage_line"
                    line = "+ {0}".format(line)
                elif index in req["addLines"]:
                    class_style += " add_line"
                    line = "+ {0}".format(line)
                else:
                    class_style += " normal_line"
                    line = "  {0}".format(line)
                content += line_str.format(class_style, index + 1, line)

            ret["code"] = 0
            ret["message"] = "获取源文件成功"
            ret["data"] = content
        else:
            ret["message"] = "git对应的信息不存在"
    return jsonify(ret)


@api_coverage.route('/<string:branch>/<string:jenkins_job>/<string:program_id>/<string:env>', methods=['GET'])
def get_branch_commit_env(branch, jenkins_job, program_id, env):
    ret = {
        "code": 1,
        "message": "获取分支提交信息失败",
        "rows": []
    }

    try:
        jenkins_info = JenkinsJob.query.filter(and_(JenkinsJob.jenkins_job_name == jenkins_job,
                                                    JenkinsJob.program_id == program_id)).first()
        if jenkins_info is not None:
            data = get_branch_commit_all(jenkins_info.gitlab_program_id, branch, env)
            ret["code"] = 0
            ret["message"] = "获取分支提交信息成功"
            ret["rows"] = data
    except:
        current_app.logger.error(traceback.format_exc())
    finally:

        return jsonify(ret)


@api_coverage.route('/jacoco_new/<string:task_id>', methods=['GET'])
def get_coverage_new(task_id):
    ret = {
        "code": 1,
        "message": "获取覆盖率报错",
        "data": False
    }
    try:
        find_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        if find_task:
            try:
                jenkins_name = json.loads(find_task.build_jenkins_jobs)[0]["name"]
            except:
                jenkins_name = find_task.build_jenkins_jobs
            jenkins_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == jenkins_name).first()
            jacoco_uuid = find_task.gitlab_program_name + "_" + find_task.build_branch + "_" + find_task.last_build_env
            commit_id = get_branch_commit(find_task.gitlab_program_id, "master")
            if not jenkins_job.git_module:
                ret["message"] = "该项目没有配置覆盖率！"
                ret["code"] = 1
                return jsonify(ret)
            elif find_task.build_task_status == 1 and commit_id != find_task.master_commit_id:
                ret["master_id"] = False
                ret["message"] = "master有分支合入，如果本分支已合入master，请发布后查看覆盖率，否则请重新构建！"
                ret["code"] = 1
                return jsonify(ret)
            elif find_task.last_build_status != 1:
                ret["message"] = "未构建成功，请构建后查看覆盖率"
                ret["code"] = 1
                return jsonify(ret)
            else:
                resp = requests.get(current_app.config["JENKINS_DICT"][jenkins_job.jenkins_url]["SUPER_JACOCO"] +
                                    current_app.config["SUPER_JACOCO_GET"] + "?uuid=" + jacoco_uuid).json()
                if resp["data"]["coverStatus"] == -1:
                    ret["code"] = 1
                    ret["message"] = resp["data"]["errMsg"]
                elif resp["data"]["coverStatus"] == 0:
                    ret["code"] = 1
                    ret["message"] = resp["data"]["errMsg"]
                    ret["data"] = resp["data"]
                elif resp["data"]["coverStatus"] == 1 and resp["data"]["lineTotal"] == 0:
                    ret["code"] = 1
                    ret["message"] = resp["data"]["errMsg"]
                elif resp["data"]["coverStatus"] == 1 and resp["data"]["lineTotal"] != 0:
                    ret["code"] = 0
                    ret["message"] = "覆盖率收集成功"
                    ret["data"] = resp["data"]
                else:
                    ret["code"] = -1
                    ret["message"] = "覆盖率收集异常"
        else:
            ret["message"] = '没有找到任务'
    except Exception as e:
        current_app.logger.error("获取覆盖率报错" + str(e))
        current_app.logger.error(traceback.format_exc())
    return jsonify(ret)
