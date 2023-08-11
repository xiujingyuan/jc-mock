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
import copy
import json
import traceback
import time

import jenkins

from app.api.build_task import api_build_task
from flask import request, jsonify, current_app
from app import db
from sqlalchemy import and_
from sqlalchemy.orm import class_mapper

from app.common.global_const import TASK_RESULT, TASK_BUILD_RESULT_BUILDING, \
    TASK_BUILD_RESULT_CANCEL, UPDATE_TASK, TASK_BUILD_RESULT_PENDING, TASK_BUILD_RESULT_QUEUE, TASK_BUILD_RESULT_FREE, \
    TASK_BUILD_RESULT_SUCCESS, TASK_BUILD_RESULT_FAILED
from app.models.AssumptBuildTaskRunDb import AssumptBuildTaskRun
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.JenkinsJobDb import JenkinsJob
from app.models.SysProgramDb import SysProgram
from app.models.TestEnvDb import TestEnv
from datetime import timedelta, date, datetime
from app.tools.tools import send_tv

base_ret = {
    "code": 0,
    "message": "成功",
    "data": None
}


@api_build_task.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Task!'


@api_build_task.route('/run/detail', methods=["GET"])
def get_task_run():
    ret = {
        "code": 1,
        "message": "获取测试任务执行情况失败",
        "data": ""
    }
    try:
        req_data = request.args
        page_size = int(req_data.get("page_size", 15))
        page_index = int(req_data.get("page_index", 1))
        program_id = int(req_data.get("program_id"))
        task_type = int(req_data.get("task_type", 1))
        now = date.today()
        query_time = now + timedelta(days=-30)

        result_paginate = AssumptBuildTask.query.filter(
            AssumptBuildTask.program_id == program_id,
            AssumptBuildTask.build_task_status == task_type,
            AssumptBuildTask.mail_receive_time >= query_time).order_by(
            AssumptBuildTask.mail_receive_time.desc()).paginate(page=page_index,
                                                                per_page=page_size,
                                                                error_out=False)
        result = result_paginate.items
        count = result_paginate.total
        task_runs = AssumptBuildTask.serialize_list(result)

        git_ids = json.loads(SysProgram.query.filter(
            SysProgram.sys_program_id == program_id).first().git_program_ids).values()
        jenkins_job_list = JenkinsJob.query.filter(JenkinsJob.gitlab_program_id.in_(git_ids)).all()
        service_name_list = list(map(lambda x: x.service_name, jenkins_job_list))
        testenv = TestEnv.query.filter(TestEnv.service_names.in_(service_name_list)).all()

        test_envs = []
        for env in testenv:
            find_env_jenkins = JenkinsJob.query.filter(JenkinsJob.service_name == env.service_names).first()
            env = TestEnv.serialize_list([env])[0]
            env["jenkins_job_name"] = find_env_jenkins.jenkins_job_name if find_env_jenkins else "not_found"
            test_envs.append(env)
        programs = JenkinsJob.query.filter(SysProgram.sys_program_id == program_id).all()
        programs_dict = {}
        for prog in programs:
            if isinstance(prog.gitlab_program_id, int):
                programs_dict[prog.gitlab_program_id] = prog.service_name
        programs_dict[0] = "not found"

        ret['page_index'] = req_data["page_index"]
        ret['rows'] = task_runs
        ret['page_size'] = len(task_runs)
        ret['total'] = count
        ret["message"] = "获取成功"
        ret["code"] = 0
        ret["test_env"] = test_envs
        ret["program"] = programs_dict
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/update', methods=["POST"])
def update_build_task_branch():
    ret = {
        "code": 1,
        "message": "更新提测任务分支错误",
        "data": ""
    }
    try:
        req_data = request.json
        if "task_id" not in req_data:
            ret["message"] += ", task_id参数是必传项"
        elif "branch" not in req_data:
            ret["message"] += ", branch参数是必传项"
        my_build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == req_data["task_id"]).first()
        if my_build_task is not None:
            my_build_task.build_branch = req_data["branch"]
            if "jenkins_job" in req_data:
                jenkins_job = req_data["jenkins_job"]
                get_jenkins = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == jenkins_job).first()
                if get_jenkins:
                    my_build_task.build_jenkins_jobs = jenkins_job
                    my_build_task.gitlab_program_id = get_jenkins.gitlab_program_id
                    my_build_task.gitlab_program_name = get_jenkins.service_name
                    if get_jenkins.git_module is not None and len(get_jenkins.git_module) > 0:
                        try:
                            last_env = my_build_task.last_build_env
                            git_modules = json.loads(get_jenkins.git_module)
                            if last_env is None:
                                last_env = list(git_modules.keys())[0]
                            if "exclude" in git_modules.get(last_env)[0].keys():
                                exclude = git_modules.get(last_env)[0]["exclude"]
                            else:
                                exclude = "test"
                        except Exception as e:
                            send_tv(e)
                            send_tv("git_module: %s" % str(jenkins_job.git_modules))
                            exclude = "test"
                    else:
                        exclude = "test"
                    my_build_task.filter_file_value = json.dumps({"exclude": exclude})
            db.session.add(my_build_task)
            db.session.flush()
            ret["data"] = my_build_task.serialize()
            ret["code"] = 0
            ret["message"] = "更新成功"
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/task_copy/<int:task_id>', methods=["GET"])
def task_copy(task_id):
    ret = copy.deepcopy(base_ret)
    try:
        build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        if build_task is not None:
            build_task_new = AssumptBuildTask()
            for item in [p.key for p in class_mapper(AssumptBuildTask).iterate_properties]:
                if item in ('id', 'run_pipeline', 'last_coverage', 'last_build_env', 'last_run_id',
                            'build_count', 'last_build_user', 'last_build_time'):
                    continue
                val = getattr(build_task, item) if item != 'last_build_status' else 0
                setattr(build_task_new, item, val)
            db.session.add(build_task_new)
            db.session.flush()
    except Exception as e:
        print(e)
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    else:
        # 获取第一页，每页15个的构建任务
        all_tasks = AssumptBuildTask.query.filter(
            AssumptBuildTask.program_id == build_task.program_id,
            AssumptBuildTask.build_task_status == build_task.build_task_status,
            AssumptBuildTask.mail_receive_time >= datetime.now() + timedelta(days=-90)).order_by(
            AssumptBuildTask.mail_receive_time.desc()).paginate(page=1,
                                                                per_page=15,
                                                                error_out=False)
        ret["total"] = all_tasks.total
        all_tasks = AssumptBuildTask.serialize_list(all_tasks.items)
        for task in all_tasks:
            if isinstance(task["build_jenkins_jobs"], str):
                pass
            else:
                task["build_jenkins_jobs"] = task["build_jenkins_jobs"][0]["name"]
            task["filter_file_value"] = json.dumps(task["filter_file_value"])
        ret["data"] = all_tasks
    return ret


@api_build_task.route('/task_cancel/<int:task_id>', methods=["GET"])
def task_cancel(task_id):
    ret = copy.deepcopy(base_ret)
    try:
        build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        if build_task is not None:
            task_run = AssumptBuildTaskRun.query.filter(
                AssumptBuildTaskRun.build_task_run_id == build_task.last_run_id,
                AssumptBuildTaskRun.build_result.in_(
                    [TASK_BUILD_RESULT_BUILDING, TASK_BUILD_RESULT_PENDING, TASK_BUILD_RESULT_QUEUE])).first()
            if task_run is not None:
                job_name = task_run.build_jenkins
                number = task_run.build_jenkins_task_id
                queue = task_run.build_jenkins_queue_id
                if job_name:
                    find_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == job_name).first()
                    if find_job is None:
                        ret["message"] = "not found the jenkins job!"
                    elif find_job.jenkins_url not in current_app.config["JENKINS_DICT"]:
                        ret["message"] = "not found the jenkins url's config!"
                    else:
                        jenkins_url = find_job.jenkins_url
                        username = current_app.config["JENKINS_DICT"][find_job.jenkins_url]["USER_ID"]
                        password = current_app.config["JENKINS_DICT"][find_job.jenkins_url]["USER_PWD"]
                        server = jenkins.Jenkins(jenkins_url, username=username, password=password)
                        queue_info = None
                        try:
                            queue_info = server.get_queue_item(task_run.build_jenkins_queue_id)
                        except:
                            pass
                        # 如果已经在构建中了，则更新build_num
                        if queue_info and \
                                queue_info["blocked"] is False and \
                                "executable" in queue_info.keys() and \
                                queue_info["executable"] is not None and \
                                queue_info["task"]["name"] == task_run.build_jenkins:
                            number = queue_info["executable"]["number"]
                        if number:
                            try:
                                server.stop_build(job_name, number)
                            except:
                                pass
                        if queue:
                            try:
                                server.cancel_queue(queue)
                            except:
                                pass
                    build_task.last_build_status = TASK_BUILD_RESULT_CANCEL
                    db.session.add(build_task)
                    task_run.build_result = TASK_BUILD_RESULT_CANCEL
                    db.session.add(task_run)
                    db.session.flush()
                    ret["code"] = 0
                    ret["message"] = "取消构建任务成功"
                else:
                    ret["message"] = "构建信息未拿到，请稍后重试"
            else:
                ret["message"] = "无可取消的构建任务"
    except:
        send_tv("取消构建异常")
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
    return jsonify(ret)


@api_build_task.route('/env/list', methods=["GET"])
def get_env_build_list():
    """
    获取对应环境最新的构建记录
    :return:返回对应的构建记录
    """
    req_data = request.args
    ret = {
        "code": 1,
        "message": "查询错误",
        "total": 0,
        'rows': []
    }
    params = []
    try:
        if req_data:
            if 'env' in req_data:
                test_env = req_data['env']
                if test_env:
                    params.append(AssumptBuildTaskRun.build_env == test_env)
            else:
                ret["message"] += "need env参数"
            if 'program_id' in req_data:
                task_run_status = req_data['program_id']
                if task_run_status:
                    params.append(AssumptBuildTaskRun.build_program_id == task_run_status)
            else:
                ret["message"] += "need build_program_id参数"
            page_index = int(req_data['page_index']) if 'page_index' in req_data else 1
            page_size = int(req_data['page_size']) if 'page_size' in req_data else 10

        current_app.logger.info("begin query, {0}".format(time.time()))
        query = AssumptBuildTaskRun.query.filter(*params)
        result = query.order_by(AssumptBuildTaskRun.id.desc()).limit(5)
        current_app.logger.info("end query, {0}".format(time.time()))
        count = 1
        current_app.logger.info("begin  serialize, {0}".format(time.time()))
        tasks = AssumptBuildTaskRun.serialize_list(result, except_attr=["build_message"])
        current_app.logger.info("end  serialize, {0}".format(time.time()))
        ret['page_index'] = page_index
        ret['rows'] = tasks
        ret['page_size'] = len(tasks)
        ret['total'] = count
        ret["message"] = "success"
        ret["code"] = 0
    except:
        current_app.logger.error(traceback.format_exc())
    finally:
        return jsonify(ret)


@api_build_task.route('/task/<string:program_name>/<int:build_task_status>', methods=["GET"])
def get_assumpt_task(program_name, build_task_status):
    ret_task = copy.deepcopy(base_ret)
    try:
        req_data = request.args
        program = SysProgram.query.filter(and_(SysProgram.sys_program_name == program_name,
                                               SysProgram.sys_is_active == 1)).first()
        # 获取第一页，每页15个的构建任务
        all_assumpt_tasks = AssumptBuildTask.query.filter(
            AssumptBuildTask.program_id == program.sys_program_id,
            AssumptBuildTask.build_task_status == build_task_status,
            AssumptBuildTask.mail_receive_time >= datetime.now() + timedelta(days=-90)).order_by(
            AssumptBuildTask.mail_receive_time.desc()).paginate(page=int(req_data["page"]),
                                                                per_page=int(req_data["limit"]),
                                                                error_out=False)
        ret_task["total"] = all_assumpt_tasks.total
        all_assumpt_tasks = AssumptBuildTask.serialize_list(all_assumpt_tasks.items)
        for task in all_assumpt_tasks:
            if isinstance(task["build_jenkins_jobs"], str):
                pass
            else:
                task["build_jenkins_jobs"] = task["build_jenkins_jobs"][0]["name"]
            task["filter_file_value"] = json.dumps(task["filter_file_value"])
        ret_task["data"] = all_assumpt_tasks
    except:
        current_app.logger.error(traceback.format_exc())
        ret_task["code"] = 1
        ret_task["message"] = traceback.format_exc()
    return jsonify(ret_task)


@api_build_task.route('/task/<int:build_task_status>', methods=["GET"])
def get_assumpt_all_task(build_task_status):
    ret_task = copy.deepcopy(base_ret)
    try:
        program = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
        program_list = tuple(map(lambda x: x.sys_program_id, program))
        # 获取第一页，每页15个的构建任务
        all_assumpt_tasks = AssumptBuildTask.query.filter(
            AssumptBuildTask.program_id.in_(program_list),
            AssumptBuildTask.build_task_status == build_task_status,
            AssumptBuildTask.mail_receive_time >= datetime.now() + timedelta(days=-90))\
            .group_by(AssumptBuildTask.story_full_id).order_by(
            AssumptBuildTask.mail_receive_time.desc()).all()
        all_assumpt_tasks = AssumptBuildTask.serialize_list(all_assumpt_tasks)
        ret_task["data"] = \
            sorted(all_assumpt_tasks, key=lambda x: (x["program_id"], x["mail_receive_time"]), reverse=False)
    except:
        current_app.logger.error(traceback.format_exc())
        ret_task["code"] = 1
        ret_task["message"] = traceback.format_exc()
    return jsonify(ret_task)


@api_build_task.route('/env/log/<int:task_id>', methods=["GET"])
def get_build_log(task_id):
    """
    获取对应构建记录的详细日志
    :return:返回对应的构建记录
    """
    ret = {
        "code": 1,
        "message": "获取对应构建记录的详细日志错误",
        "data": "",
        'log': ""
    }
    try:
        build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        task_details = AssumptBuildTaskRun.query.filter(
            AssumptBuildTaskRun.build_task_run_id == build_task.last_run_id).first()
        if task_details:
            ret["code"] = 0
            ret["message"] = "获取构建记录成功"
            ret["log"] = task_details.build_message
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/status/<int:task_id>', methods=["GET"])
def get_build_task_status(task_id):
    """
    获取对应构建记录的详细日志
    :return:返回对应的构建记录
    """
    ret_task = copy.deepcopy(base_ret)
    build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
    build_task_run = AssumptBuildTaskRun.query.filter(
        AssumptBuildTaskRun.build_task_run_id == build_task.last_run_id).first()
    ret_task["data"] = dict()
    ret_task["data"]["env"] = build_task_run.build_env
    ret_task["data"]["url"] = build_task_run.build_message
    ret_task["data"]["result"] = build_task.last_build_status
    return jsonify(ret_task)


@api_build_task.route('/get_env/<int:task_id>', methods=["GET"])
def get_can_use_env(task_id):
    """
    获取对应构建记录的详细日志
    :return:返回对应的构建记录
    """
    ret = {
        "code": 1,
        "message": "获取对应的可用环境失败",
        "data": "",
    }
    try:
        task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        jenkins_job_name_list = list(map(lambda x: x["name"], json.loads(task.build_jenkins_jobs)))
        jenkins_job_list = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name.in_(jenkins_job_name_list)).all()
        service_name_list = list(map(lambda x: x.service_name, jenkins_job_list))
        env_list = TestEnv.query.filter(TestEnv.service_names.in_(service_name_list)).all()

        tasks = TestEnv.serialize_list(env_list)
        ret["code"] = 0
        ret["message"] = "获取环境正确"
        ret["data"] = tasks
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/get_env_status/<int:task_id>/<string:env>', methods=["GET"])
def get_env_status(task_id, env):
    """
    获取对应构建环境的情况
    :return:返回对应的构建环境的情况
    """
    ret = {
        "code": 1,
        "message": "获取对应的构建环境的情况",
        "data": "",
    }
    try:
        task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        build_jenkins = task.build_jenkins_jobs
        dev_info = TestEnv.query.filter(and_(TestEnv.env_id == env,
                                             TestEnv.service_names == task.gitlab_program_name)).first()
        if dev_info:
            if dev_info.run_branch and dev_info.run_branch != task.build_branch:
                dev_run_info = AssumptBuildTaskRun.query.filter(
                    AssumptBuildTaskRun.build_jenkins == build_jenkins,
                    AssumptBuildTaskRun.build_env == env).order_by(
                    AssumptBuildTaskRun.id.desc()).first()
                if dev_run_info:
                    ret["data"] = "环境【{0}】在【{1}】被【{2}】构建过, 构建分支为:【{3}】,是否继续构建？".format(
                        env,
                        dev_run_info.build_time,
                        dev_run_info.build_user,
                        dev_run_info.build_branch)
                    ret["code"] = 2
                else:
                    ret["data"] = "not found the env's build record!"
                    ret["code"] = 3
            else:
                ret["data"] = ""
                ret["code"] = 0
            ret["message"] = "获取环境正确"
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/assumpt_task/update/', methods=["POST"])
def assumpt_task_update():
    ret = {
        "code": 1,
        "message": "获取对应的Jenkins任务失败",
        "data": "",
    }
    req = request.json
    task_id = req.pop("task_id")
    task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
    if task is None:
        ret['message'] = 'not found the task!'
    else:
        for kev in req:
            if hasattr(task, kev):
                value = req[kev]
                value = value if isinstance(value, str) else json.dumps(value)
                setattr(task, kev, value)
        if "build_jenkins_jobs" in req and len(req["build_jenkins_jobs"])>0 and req["build_jenkins_jobs"] is not None:
            jenkins_job = req["build_jenkins_jobs"]
            get_jenkins = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == jenkins_job).first()
            if get_jenkins:
                task.gitlab_program_id = get_jenkins.gitlab_program_id
                task.gitlab_program_name = get_jenkins.service_name
        db.session.add(task)
        db.session.flush()
        ret['data'] = task.serialize()
        ret['code'] = 0
    return jsonify(ret)


@api_build_task.route('/assumpt_task/get_info/', methods=["POST"])
def assumpt_task_get_info():
    ret = {
        "code": 1,
        "message": "获取对应的Jenkins任务失败",
        "data": "",
    }
    req = request.json
    task_id = req.pop("task_id")
    task_attr = req.pop("attr")
    task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
    if task is None:
        ret['message'] = 'not found the task!'
    else:
        if hasattr(task, task_attr):
            value = getattr(task, task_attr)
            value = json.loads(value) if value else {}
            ret['data'] = value
            ret['code'] = 0
        else:
            ret['message'] = 'not found the attr!'
    return jsonify(ret)


@api_build_task.route('/get_jenkins/<string:program_name>', methods=["GET"])
def get_task_jenkins_names(program_name):
    """
    获取对应任务的所有可能的Jenkins任务
    """
    ret = copy.deepcopy(base_ret)
    ret["data"] = dict()
    try:
        program = SysProgram.query.filter(SysProgram.sys_program_name == program_name).first()
        program_git = json.loads(program.git_program_ids).values()
        get_jenkins = JenkinsJob.query.filter(JenkinsJob.gitlab_program_id.in_(program_git),
                                              JenkinsJob.is_active == 1).all()
        for item in get_jenkins:
            env_list = TestEnv.query.filter(TestEnv.service_names == item.service_name).all()
            env_list = list(map(lambda x: x.env_id, env_list))
            ret["data"][item.jenkins_job_name] = {"service_name": item.service_name,
                                                  "filter": {"exclude": "test"},
                                                  "env": env_list}
        ret["code"] = 0
    except:
        ret["code"] = 1
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_build_task.route('/get_log/<int:task_id>', methods=["GET"])
def get_log_url(task_id):
    """
    获取对应任务的所有可能的Jenkins任务
    :param task_id: 需要查询的构建任务id
    :return:
    """
    ret = {
        "code": 1,
        "msg": "获取日志地址错误",
        "url": "",
    }
    try:
        get_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        if get_task is not None:
            get_run = AssumptBuildTaskRun.query.filter(and_(AssumptBuildTaskRun.build_task_id == get_task.id,
                                                            AssumptBuildTaskRun.build_message != '',
                                                            AssumptBuildTaskRun.build_message.isnot(None)
                                                            )).order_by(AssumptBuildTaskRun.id.desc()).first()
            if get_run:
                ret["url"] = get_run.build_message
                ret["msg"] = "获取日志地址成功"
                ret["code"] = 0
            else:
                ret["msg"] = "没有找到对应的日志信息"
    except:
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
        ret["msg"] = traceback.format_exc()

    return jsonify(ret)


def get_sys_program_git_ids(program_id):
    program = SysProgram.query.filter(SysProgram.sys_program_id == program_id).first()
    list(json.loads(program["git_program_ids"]).values)
