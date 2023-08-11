#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/09
 @file: task_view.py
 @site:
 @email:
"""
import datetime
import json
import traceback
import uuid

from flask import jsonify, request, current_app
from app import db
from app.common.Coverage import get_branch_commit
from app.common.global_const import TASK_BUILD_RESULT_PENDING, TASK_BUILD_RESULT_BUILDING, TASK_BUILD_RESULT_QUEUE
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.AssumptBuildTaskRunDb import AssumptBuildTaskRun
from app.models.JenkinsJobDb import JenkinsJob
from app.models.TestEnvDb import TestEnv
from app.tasks import task_url
from app.tools.tools import send_tv
from app.tasks.build_task.build_task import run_auto_task
from app.tasks.common_task.calc_count import calc_count_task


@task_url.route("/build_task_create/<build_task_id>", methods=["POST"])
def build_task_create(build_task_id):
    ret = {
        "code": 0,
        "url": "",
        "message": "构建成功",
        "run_id": 0
    }
    try:
        req_data = request.json
        print(req_data)
        if not req_data['job_name']:
            ret["message"] += ", job_name 不能为空！"
        elif not req_data['build_branch']:
            ret["message"] += ", 构建分支不能为空"
        else:
            env_id = req_data["env"]["num"]
            branch = req_data["build_branch"]
            job_name = req_data['job_name']
            build_user = req_data["build_user"]
            req_data["env"]["Jacoco_Branch"] = branch
            assumpt_build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == build_task_id).first()
            jenkins_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == req_data['job_name']).first()

            if jenkins_job is None:
                ret["message"] = "error, not found the job's info"
            elif assumpt_build_task.last_build_status in (TASK_BUILD_RESULT_PENDING,
                                                          TASK_BUILD_RESULT_BUILDING,
                                                          TASK_BUILD_RESULT_QUEUE):
                ret["message"] = "error, task is building, pls wait"
            else:
                current_env = TestEnv.query.filter(TestEnv.env_id == env_id,
                                                   TestEnv.service_names == jenkins_job.service_name).first()
                if current_env is None:
                    ret["message"] = "error, not found the program's env"
                else:
                    task_run_id = str(uuid.uuid4())

                    # 获取master当前commit
                    commit_id = get_branch_commit(jenkins_job.gitlab_program_id, "master")

                    # 修改主表信息
                    assumpt_build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == build_task_id).first()
                    assumpt_build_task.build_count += 1
                    assumpt_build_task.last_run_id = task_run_id
                    assumpt_build_task.last_build_user = build_user
                    assumpt_build_task.last_build_status = TASK_BUILD_RESULT_PENDING
                    assumpt_build_task.last_build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    assumpt_build_task.last_build_env = env_id
                    assumpt_build_task.build_jenkins_jobs = job_name
                    assumpt_build_task.service_name = jenkins_job.service_name
                    assumpt_build_task.master_commit_id = commit_id
                    db.session.add(assumpt_build_task)
                    db.session.flush()

                    # 新增一条构建信息，状态为初始化
                    assumpt_build_task_run = AssumptBuildTaskRun()
                    assumpt_build_task_run.build_task_id = build_task_id
                    assumpt_build_task_run.build_task_run_id = task_run_id
                    assumpt_build_task_run.build_user = build_user
                    assumpt_build_task_run.build_jenkins = job_name
                    assumpt_build_task_run.build_branch = branch
                    assumpt_build_task_run.build_env = env_id
                    assumpt_build_task_run.build_result = TASK_BUILD_RESULT_PENDING
                    assumpt_build_task_run.build_param = json.dumps(req_data)
                    assumpt_build_task_run.build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    assumpt_build_task_run.iteration_id = assumpt_build_task.iteration_id
                    db.session.add(assumpt_build_task_run)
                    db.session.flush()

                    # 等到以上操作完全正确再记录测试环境对应的分支
                    current_env.run_branch = branch
                    db.session.add(current_env)
                    db.session.flush()
    except Exception as e:
        send_tv(traceback.format_exc())
        current_app.logger.error(e)
        current_app.logger.error(traceback.format_exc())
        ret["code"] = 1
        ret["message"] = "{0}".format(traceback.format_exc())
    return jsonify(ret)


@task_url.route('/exec_auto_task/<int:task_id>/<int:env>', methods=["GET"])
def exec_auto_task(task_id, env):
    ret = {
        "code": 0,
        "message": "自动化成功"
    }
    try:
        run_auto_task.apply_async(args=[task_id, env])
    except Exception as e:
        ret['code'] = 1
        ret["message"] = e
    finally:
        return jsonify(ret)
