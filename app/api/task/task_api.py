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
import math
import traceback
import time

import requests
import json

from app.api.case.case_api import get_sys_program
from app.api.task import api_task
from flask import request, jsonify, current_app
from app import db
from sqlalchemy import and_

from app.models.ProgramBusinessDb import ProgramBusiness
from app.models.TestTasksCasesDb import TestTasksCase
from app.models.TestTasksDb import TestTask
from app.models.TestTasksRunDb import TestTasksRun
from app.tasks.task_view import run_case_by_task


@api_task.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Task!'


@api_task.route('/create', methods=['POST'])
def create_task():
    """
    根据传入的任务标题，创建人，用例ID创建用例集任务
    :return: 返回创建成功/失败
    """
    req_data = request.json
    ret = {
        "code": 1,
        "msg": "update error",
        "task_id": ""
    }

    if "task_title" not in req_data:
        ret["msg"] = "task_title必须传"
    elif "task_ids" not in req_data:
        ret["msg"] = "task_ids必须传"
    elif "task_create_user" not in req_data:
        ret["msg"] = "task_create_user必须传"
    else:
        try:
            mytask = TestTask()
            mytask.task_title = req_data["task_title"]
            mytask.task_create_user = req_data["task_create_user"]
            mytask.task_last_user = req_data["task_create_user"]
            mytask.task_version = int(round(time.time() * 1000))
            mytask.task_business = req_data["task_business"] if "task_business" in req_data else ""
            mytask.task_system = req_data["task_system"] if "task_system" in req_data else ""
            mytask.task_type = 0 if "debug" in req_data and req_data["debug"] else 1
            db.session.add(mytask)
            db.session.flush()
            for case_id in req_data["task_ids"]:
                task_case = TestTasksCase()
                task_case.task_id = mytask.task_id
                task_case.case_id = case_id
                task_case.task_version = mytask.task_version
                db.session.add(task_case)
            db.session.flush()
            ret["task_id"] = mytask.task_id
            ret["msg"] = "success"
            ret["code"] = 0
            # if "debug" in req_data and req_data["debug"]:
            #     # 执行该用例集
            #     code, location, msg, run_id = run_case_by_task(mytask.task_id)
            #     if not code == 202:
            #         ret["msg"] = "创建用例集成功，执行失败！"
            #         ret["code"] = 1
        except:
            current_app.logger.error(traceback.format_exc())

    return jsonify(ret)


@api_task.route('/all', methods=['GET'])
def task_all():
    """
    获取所有任务的信息
    :return: 返回所有信息
    """
    req_data = request.args
    ret = {
        "code": 1,
        "message": "查询错误",
        "total": 0,
        'rows': []
    }
    print("task_all", req_data)
    params = []
    try:
        if req_data:
            if 'txt_task_title' in req_data:
                task_title = req_data['txt_task_title']
                if task_title:
                    params.append(TestTask.task_title.like('%' + task_title + '%'))
            if 'txt_task_run_status' in req_data:
                task_run_status = req_data['txt_task_run_status']
                if task_run_status:
                    params.append(TestTask.task_last_run_id == task_run_status)
            if 'txt_task_des' in req_data:
                task_des = req_data['txt_task_des']
                if task_des:
                    params.append(TestTask.task_desc == task_des)
            if "txt_from_system" in req_data:
                from_system = req_data['txt_from_system']
                if from_system:
                    params.append(TestTask.task_system == int(from_system))
            if "txt_actor" in req_data:
                actor = req_data['txt_actor']
                if actor:
                    params.append(TestTask.task_create_user == actor)
            page_index = int(req_data['page_index']) if 'page_index' in req_data else 1
            page_size = int(req_data['page_size']) if 'page_size' in req_data else 20
        query = TestTask.query.filter(*params)
        result_paginate = query.order_by(TestTask.task_id.desc()).paginate(page=page_index,
                                                                           per_page=page_size,
                                                                           error_out=False)
        result = result_paginate.items
        count = result_paginate.total
        tasks = TestTask.serialize_list(result)

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


@api_task.route("/detail/<int:task_id>", methods=["GET"])
def task_detail(task_id):
    """
    获取对应任务ID的详情
    :param task_id: 任务ID
    :return: json 返回对应的任务详情
    """
    ret = {
        "code": 1,
        "message": "获取任务详情错误",
        "data": "",
        'rows': []
    }
    try:
        task_details = TestTask.query.filter(TestTask.task_id == task_id)
        if task_details:
            req_data = request.args
            page_index = int(req_data['page_index']) if 'page_index' in req_data else 1
            page_size = int(req_data['page_size']) if 'page_size' in req_data else 20

            result_paginate = TestTasksRun.query.filter(TestTasksRun.task_id == task_id).order_by(
                TestTasksRun.run_id.desc()).paginate(page=page_index,
                                                     per_page=page_size,
                                                     error_out=False)

            result = result_paginate.items
            count = result_paginate.total
            task_runs = TestTasksRun.serialize_list(result)

            ret['page_index'] = page_index
            ret['rows'] = task_runs
            ret['page_size'] = len(task_runs)
            ret['total'] = count
            ret["message"] = "success"
            ret["code"] = 0
            ret["data"] = TestTask.serialize(task_details[0])
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_task.route('/run/update', methods=["POST"])
def update_run_log():
    """
    更新对应任务的执行日志
    :return: 返回更新状态
    """
    ret = {
        "code": 1,
        "message": "更新任务执行日志错误",
        "data": ""
    }
    try:
        req_data = request.json
        if "task_id" not in req_data:
            ret["message"] += ", task_id参数是必传项"
        elif "task_run_id" not in req_data:
            ret["message"] += ", task_run_id参数是必传项"
        else:
            task_run_detail = TestTasksRun.query.filter(and_(TestTasksRun.task_id == req_data["task_id"],
                                                             TestTasksRun.run_task_id == req_data["task_run_id"])).one()
            if task_run_detail:
                if "log" in req_data:
                    if task_run_detail.run_result is None:
                        task_run_detail.run_result = ""
                    if req_data["log"] not in task_run_detail.run_result:
                        task_run_detail.run_result += req_data["log"] + "\r\n"
                elif "run_status" in req_data:
                    task_run_detail.run_status = req_data["run_status"]

                    test_task = TestTask.query.filter(TestTask.task_id == req_data["task_id"]).one()
                    test_task.task_last_result = 1 if int(req_data["run_status"]) == 2 else 0
                    test_task.task_status = 0
                    db.session.add(test_task)

                db.session.add(task_run_detail)
                db.session.flush()
                ret["message"] = "更新成功"
                ret["code"] = 0
            else:
                ret["message"] = "未找到对应任务记录"
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_task.route('/run/detail', methods=["GET"])
def get_task_run():
    """
    获取任务运行时的详情
    :return: 返回运行时的详情
    """
    ret = {
        "code": 1,
        "message": "获取测试任务执行情况失败",
        "data": ""
    }
    try:
        req_data = request.args
        if "page" not in req_data:
            ret["message"] += ", page参数是必传项"
        elif "task_id" not in req_data:
            ret["message"] += ", task_id参数是必传项"
        else:
            task_run_detail = TestTasksRun.query.filter(TestTasksRun.task_id == req_data["task_id"]).all()
            if task_run_detail:
                result = TestTasksRun.query.filter(TestTasksRun.task_id == req_data["task_id"]).order_by(
                    TestTasksRun.run_id.desc()).limit(5)
                task_runs = TestTasksRun.serialize_list(result)

                ret['page_index'] = req_data["page"]
                ret['data'] = task_runs
                ret['page_size'] = 5
                ret['total'] = 1
                ret["message"] = "获取成功"
                ret["code"] = 0
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


@api_task.route('/run_case/', methods=["GET"])
def get_task_run_case():
    """
    获取任务运行时用例的执行情况
    :return: 获取任务运行时用例的执行情况
    """
    ret = {
        "code": 1,
        "message": "获取测试任务执行情况失败",
        "data": ""
    }
    try:
        req_data = request.args
        if "page_index" not in req_data:
            ret["message"] += ", page_index参数是必传项"
        if "task_id" not in req_data:
            ret["message"] += ", task_id参数是必传项"
        if "page_size" not in req_data:
            ret["message"] == ", page_size参数是比传项"
        else:
            result_paginate = TestTasksCase.query.filter(TestTasksCase.task_id == req_data["task_id"]).paginate(
                page=int(req_data["page_index"]),
                per_page=int(req_data["page_size"]),
                error_out=False)
            if result_paginate:
                result_case_id_list = []

                for item in result_paginate.items:
                    result_case_id_list.append(item.case_id)

                url = "{0}/case/search".format(current_app.config["BACKEND_URL"])
                headers = {'content-type': 'application/json'}
                json_data = {
                    "case_ids": result_case_id_list
                }
                req = requests.post(url, data=json.dumps(json_data), headers=headers)
                if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                    ret_data = req.json()
                    current_app.logger.info(ret_data)
                    if "data" in ret_data and "cases" in ret_data["data"]:
                        ret["code"] = 0
                        ret["message"] = "查询成功"

                        # search_cases = ret_data["data"]["cases"]
                        # for item_case in search_cases:
                        #     item_case["case_from_system_name"], item_case["case_belong_business_name"] = \
                        #         get_system_business_name(item_case["case_from_system"],
                        #                                  item_case["case_belong_business"])
                        search_cases = ret_data["data"]["cases"]
                        get_system_business_name(search_cases)

                        ret["rows"] = search_cases
                        ret["total"] = ret_data["data"]["total"]
                        ret['page_index'] = req_data["page_index"]
                        ret['page_size'] = req_data["page_size"]
                        ret["message"] = "获取成功"
                        ret["code"] = 0
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)


def get_system_business_name(search_cases, history=False):
    sys_programs = get_sys_program()

    def get_cname(sys_program_id):
        for program in sys_programs:
            if program["sys_program_id"] == sys_program_id:
                return program["sys_program_name"]
        return ""

    all_business = ProgramBusiness.query.all()

    def get_business_name(sys_program_id, business_name):
        for business in all_business:
            if business.program_id == sys_program_id and business.business_name == business_name:
                return business.business_cname
        return ""
    case_name = "history_case_from_system" if history else "case_from_system"
    business_name = "history_case_belong_business" if history else "case_belong_business"
    for item_case in search_cases:
        item_case["{0}_name".format(case_name)] = get_cname(item_case[case_name])
        item_case["{0}_name".format(business_name)] = get_business_name(item_case[case_name],
                                                                        item_case[business_name])


@api_task.route('/run_case/result/<int:task_id>/<string:build_id>', methods=["GET"])
def get_task_run_case_result(task_id, build_id):
    """
    获取任务运行时用例的执行情况
    :return: 获取任务运行时用例的执行情况
    """
    ret = {
        "code": 1,
        "message": "获取测试任务执行情况失败",
        "data": "",
        "rows": [],
        "finish": 0,
        "env": ""
    }
    try:
        headers = {'content-type': 'application/json'}
        req_data = request.args
        url = "{0}/history/run_case/{1}".format(current_app.config["BACKEND_URL"], build_id)
        test_task = TestTasksRun.query.filter(and_(TestTasksRun.task_id == task_id,
                                                   TestTasksRun.run_task_id == build_id)).first()
        ret["finish"] = 1 if test_task and test_task.run_status in (2, 3) else 0
        ret['env'] = test_task.run_env_num
        req = requests.get(url, data=json.dumps(req_data), headers=headers)
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            ret_data = req.json()
            current_app.logger.info(ret_data)
            if "data" in ret_data:
                ret["code"] = 0
                ret["message"] = "查询成功"
                test_run_cases = ret_data["data"][0]["cases"]
                get_system_business_name(test_run_cases, history=True)
                ret["rows"] = test_run_cases
                ret["total"] = ret_data["data"][0]["total"]
                ret['page_index'] = ret_data["data"][0]["page_index"]
                ret['page_size'] = ret_data["data"][0]["page_size"]
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()

    return jsonify(ret)


@api_task.route('/run_case/result/<string:build_id>/<string:exec_group>', methods=["GET"])
def get_task_run_case_result_sub(build_id, exec_group):
    """
    获取任务运行时用例的执行情况
    :return: 获取任务运行时用例的执行情况
    """
    ret = {
        "code": 1,
        "message": "获取测试任务执行情况失败",
        "data": "",
        "rows": [],
        "finish": 0
    }
    try:
        headers = {'content-type': 'application/json'}
        req_data = request.args
        url = "{0}/history/run_case/{1}/{2}/".format(current_app.config["BACKEND_URL"], build_id, exec_group)
        req = requests.get(url, headers=headers)
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            ret_data = req.json()
            if "data" in ret_data:
                ret["code"] = 0
                ret["message"] = "查询成功"
                test_run_cases = ret_data["data"][0]
                get_system_business_name(test_run_cases, history=True)
                ret["rows"] = test_run_cases
                ret["total"] = len(ret_data["data"][0])
                ret['page_index'] = req_data["page_index"]
                ret['page_size'] = req_data["page_size"]
    except:
        current_app.logger.error(traceback.format_exc())
        ret["message"] = traceback.format_exc()
    return jsonify(ret)
