#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/10
 @file: case_task.py
 @site:
 @email:
"""
import json
import random

import requests
from celery_once import QueueOnce
from app import celery
from flask import current_app
import jenkins
import traceback
import time
from app import db
import copy
from app.models.TestTasksDb import TestTask
from app.models.TestTasksRunDb import TestTasksRun


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_case_by_case_id(self, case_id, build_task_id):
    """

    :param self:
    :param case_id:
    :param build_task_id:
    :return:
    """
    try:
        email = "zhangtingli@kuainiugroup.com"
        current_app.logger.info("case_id args is {0}".format(case_id))
        current_app.logger.info("case_id email is {0} ".format(email))
        exec_case_array_str = ','.join(str(case) for case in case_id)
        total = len(case_id) * 10

        calc_url = "{0}/case/calculate".format(current_app.config["BACKEND_URL"])
        print(calc_url)
        headers = {'content-type': 'application/json'}
        req = requests.get(calc_url, data=json.dumps({"case_id": case_id}), headers=headers).json()
        print(req)

        i = 0
        total = 3 + req["data"]
        result = "SUCCESS"
        run_job = "no jenkins job"
        server = jenkins.Jenkins(current_app.config["JENKINS_URL"],
                                 current_app.config["USER_ID"],
                                 current_app.config["USER_PWD"])

        print(server.get_running_builds(), type(server.get_running_builds()))

        running_job = list(map(lambda x: x["name"], server.get_running_builds()))

        can_user_job = copy.deepcopy(current_app.config["JENKINS_RUN_JOB"])

        print("running_job", can_user_job)
        for job in can_user_job:
            if job in running_job:
                can_user_job.remove(job)
        print("can_user_job", can_user_job)

        if not can_user_job:
            run_job = random.choice(current_app.config["JENKINS_RUN_JOB"])
            print("can_user_job full:", can_user_job)
        else:
            run_job = random.choice(can_user_job)
            print("run_job", run_job)
        next_build_number = server.get_job_info(run_job)['nextBuildNumber']

        current_app.logger.info("before request id is: {0} {1}".format(self.request.id, type(self.request.id)))
        build_number = server.build_job(run_job,
                                        parameters={"case_ids": exec_case_array_str,
                                                    "email_address": email,
                                                    "current_build_id": self.request.id})

        current_app.logger.info("case id is: {0}".format(exec_case_array_str))
        current_app.logger.info("request id is: {0} {1}".format(self.request.id, type(self.request.id)))
        save_build_message(self.request.id, "", next_build_number, build_task_id, run_job)
        now = time.time()
        console_output = ""
        while True:
            try:
                build_info = server.get_build_info(run_job,
                                                   next_build_number)
                console_output = server.get_build_console_output(run_job,
                                                                 next_build_number)
            except:
                console_output = ""
                pass
            else:
                console_output = console_output.strip("\r\n").strip("\n")
                if console_output:
                    self.update_state(state='PROGRESS',
                                      meta={'current': i,
                                            'total': total,
                                            'status': console_output,
                                            'build_num': next_build_number})
                    if "Started by user" in console_output:
                        i = 1
                    if "------------------------get case!------------------------------" in console_output:

                        i = 2
                    if "主用例 初始化/前置任务 开始" in console_output:
                        i += console_output.count("主用例 初始化/前置任务 开始")
                    if "开始执行子用例，父用例ID：" in console_output:
                        i += console_output.count("开始执行子用例，父用例ID：")
                if not build_info["building"]:
                    break
                time.sleep(0.1)
                if time.time() - now >= 1:
                    now = time.time()
                    save_build_message(self.request.id, console_output, next_build_number, build_task_id, run_job)

        while True:
            time.sleep(1)
            console_output = server.get_build_console_output(run_job, next_build_number)
            console_output_list = console_output.strip("\n").split("\n")
            current_app.logger.info("console_output_list[-1] {0}".format(console_output_list[-1]))
            if console_output_list[-1].startswith("Finished:"):
                if "failure" in console_output.lower():
                    result = "FAILURE"
                # current_app.logger.info(console_output)
                current_app.logger.info(build_task_id)
                save_build_message(self.request.id, console_output, next_build_number, build_task_id, run_job, result)
                break
        self.update_state(state="SUCCESS",
                          meta={'current': total,
                                'total': total,
                                'result': result,
                                'status': console_output,
                                'build_num': next_build_number})
        time.sleep(1)
    except jenkins.JenkinsException:
        current_app.logger.error("jenkins的的参数错误！")
        save_build_message(self.request.id, console_output, next_build_number, build_task_id, run_job, "FAILURE")
        self.update_state(state='FAILURE',
                          meta={'current': i,
                                'total': total,
                                'result': 'error',
                                'status': "jenkins任务构建失败",
                                'build_num': next_build_number})
    except Exception as e:
        current_app.logger.exception(e)
        save_build_message(self.request.id, console_output, next_build_number, build_task_id, run_job, "FAILURE")
        self.update_state(state='FAILURE',
                          meta={'current': i,
                                'total': total,
                                'result': 'error',
                                'status': traceback.format_exc(),
                                'build_num': next_build_number})


def save_build_message(run_id, message, next_build_number, build_task_id, jenkins_job, result="PROCESS"):
    try:
        current_app.logger.info("run_id: {0}, next_build_number: {1}, build_task_id: {2}, result: {3}".format(
            run_id,
            next_build_number,
            build_task_id,
            result
        ))

        build_task = TestTasksRun.query.filter(TestTasksRun.run_task_id == run_id).first()
        build_task_parent = TestTask.query.filter(TestTask.task_last_run_id == run_id).first()

        if build_task and message:
            build_task.run_result = message
            build_task.run_jenkins_task_id = next_build_number
            build_task.run_jenkins_job = jenkins_job
            if result == "FAILURE":
                build_task.run_status = 3
                if build_task_parent:
                    build_task_parent.task_last_result = 0
                    build_task_parent.task_status = 0
                build_task.run_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            elif result == "SUCCESS":
                build_task.run_status = 2
                if build_task_parent:
                    build_task_parent.task_last_result = 1
                    build_task_parent.task_status = 0
                build_task.run_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.session.add(build_task)
            if build_task_parent:
                db.session.add(build_task_parent)
            db.session.flush()
            
    except:
        current_app.logger.error(traceback.format_exc())

