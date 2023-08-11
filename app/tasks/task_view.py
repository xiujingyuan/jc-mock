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
from flask import jsonify, request, render_template, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy import and_
from app import db
from app.models.SysProgramDb import SysProgram
from app.models.TestTasksCasesDb import TestTasksCase
from app.models.TestTasksDb import TestTask
from app.models.TestTasksRunDb import TestTasksRun
from app.models.UserModel import User
from app.base.views import BaseView
from app.tasks.case.case_task import run_case_by_case_id
from app.tasks.test.test_task import long_task
from app.tasks import task_url
import requests
import json
import os


@task_url.route("/status/<task_id>")
def task_status(task_id):
    headers = {'content-type': 'application/json'}
    url = '{0}/tasks/status/{1}'.format(current_app.config["BACKEND_URL"], task_id)
    result = requests.get(url, headers=headers)
    return jsonify(result.json())


@task_url.route("/test")
def task_test():
    return render_template(current_app.config["THEME_URL"] +"task/testv3.html")


@task_url.route("/long_task", methods=["GET"])
def task_create():
    headers = {'content-type': 'application/json'}
    url = '{0}/tasks/long_task'.format(current_app.config["BACKEND_URL"])
    result = requests.get(url, headers=headers)
    return jsonify({}), result.status_code, result.json()


@task_url.route("/case_task_status/status/<string:task_run_id>", methods=["GET"])
def case_task_status(task_run_id):
    task = run_case_by_case_id.AsyncResult(task_run_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...',
            'message': ''
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0) if task.info is not None else 1,
            'total': task.info.get('total', 1) if task.info is not None else 1,
            'status': task.info.get('status', '') if task.info is not None else "",
            'message': task.info.get('message', '') if task.info is not None else ""
        }

    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': "",
            'message': "failed"
        }
    return jsonify(response)


@task_url.route("/case_task_create/<int:task_id>", methods=["GET"])
def case_task_create(task_id):
    ret = {
        "code": 303,
        "url": "",
        "message": "",
        "run_id": "",
        "build_id": ""
    }
    if "user" not in request.args:
        ret["message"] = "not found the user"
    else:
        task_run_env = request.args["task_run_env"] if "task_run_env" in request.args else None
        user = request.args["user"]
        run_task = TestTask.query.filter(TestTask.task_id == task_id).first()
        if run_task is not None:
            run_task_program = SysProgram.query.filter(SysProgram.sys_program_id == run_task.task_system).first()
            if run_task_program is not None:
                # 更新对应全局变量的值
                if run_task_program.sys_env_params is None:
                    ret["code"], ret["url"], ret["message"], ret["run_id"], ret["build_id"] = run_case_by_task(
                        task_id, None)
                elif run_task_program.sys_env_params:
                    if not task_run_env:
                        headers = {'content-type': 'application/json'}
                        req_task_run_env = requests.post("{0}/params/search".format(current_app.config["BACKEND_URL"]),
                                                         data=json.dumps({"name": run_task_program.sys_env_params}),
                                                         headers=headers)
                        if req_task_run_env.status_code == 200 and "code" in req_task_run_env.json() and \
                                req_task_run_env.json()["code"] == 0:
                            for item in req_task_run_env.json()["data"]["params"]:
                                if item["name"] == run_task_program.sys_env_params:
                                    default_run_env = item['value']
                                    break
                            ret["code"], ret["url"], ret["message"], ret["run_id"], ret["build_id"] = run_case_by_task(
                                task_id, default_run_env)
                        else:
                            ret["message"] = "get the global param's value failed!"
                    else:
                        req_change = requests.post("{0}/params/{1}/{2}/{3}".format(current_app.config["BACKEND_URL"],
                                                                                   run_task_program.sys_env_params,
                                                                                   task_run_env,
                                                                                   user))
                        if req_change.status_code == 200 and json.loads(req_change.text)["code"] == 0:
                            ret["code"], ret["url"], ret["message"], ret["run_id"], ret["build_id"] = run_case_by_task(
                                task_id, task_run_env)
                        else:
                            ret["message"] = "change the global param failed"
                else:

                    ret["message"] = "the task's global params is null"

            else:
                ret["message"] = "not found the task's program"
    return jsonify(ret)


def run_case_by_task(task_id, task_run_env):
    """
    创建执行自动化用例集任务
    :param task_id: 用例集任务ID
    :param task_run_env:本次运行的环境ID
    :return:
    """
    headers = {'content-type': 'application/json'}
    msg = "success"
    code = ""
    location = ""
    run_id = 0
    build_id = ""
    run_cases = TestTasksCase.query.filter(TestTasksCase.task_id == task_id).all()
    run_cases = list(map(lambda x: x.case_id, run_cases))

    # url = '{0}/tasks/case_task_create/'.format(current_app.config["BACKEND_URL"])
    try:
        # result = requests.post(url, headers=headers, data=json.dumps(run_cases))
        task = run_case_by_case_id.apply_async(args=[run_cases, task_id])
        code = 202
        location = '/tasks/case_task_status/status/{0}'.format(task.id)
        run_task_id = task.id

        test_task_run = TestTasksRun()
        test_task_run.task_id = task_id
        test_task_run.run_task_id = run_task_id
        test_task_run.run_env_num = task_run_env
        db.session.add(test_task_run)

        run_id = test_task_run.run_id
        build_id = test_task_run.run_task_id

        test_task = TestTask.query.filter(TestTask.task_id == task_id).one()
        test_task.task_run_time += 1
        test_task.task_last_run_id = run_task_id
        test_task.task_last_run_time = test_task_run.run_begin
        test_task.task_last_run_env = task_run_env
        test_task.task_status = 1
        db.session.add(test_task)
        db.session.flush()
    except Exception as e:
        code = 303
        msg = e

    finally:
        return code, location, msg, run_id, build_id


class TaskView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] +'task/test/test_task.html', **self.context)


task_url.add_url_rule('/index', view_func=TaskView.as_view('task'))


class TaskListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'task/task_list.html', **self.context)


task_url.add_url_rule('/list', view_func=TaskListView.as_view('task_list'))


class TaskCreateView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'task/task_create.html', **self.context)


task_url.add_url_rule('/create', view_func=TaskCreateView.as_view('task_created'))

