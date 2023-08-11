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
from celery_once import QueueOnce
from app import celery, db
from flask import current_app
import jenkins
import traceback

from app.common.global_const import TASK_BUILD_RESULT_FAILED, TASK_BUILD_RESULT_SUCCESS, \
    TASK_BUILD_RESULT_CANCEL, TASK_BUILD_RESULT_BUILDING, TASK_BUILD_RESULT_PENDING, TASK_BUILD_RESULT_QUEUE
from app.models.AssumptBuildTaskRunDb import AssumptBuildTaskRun
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.JenkinsJobDb import JenkinsJob
import os

from app.models.KeyValueDb import KeyValue
from app.tasks.coverage_task.coverage_task import trigger_build_coverage
from app.tools.tools import send_tv


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_build_task(self):
    current_app.logger.info("开始更新构建任务状态")
    try:
        build_task_run_list = AssumptBuildTaskRun.query.filter(
            AssumptBuildTaskRun.build_result.in_([TASK_BUILD_RESULT_BUILDING,
                                                  TASK_BUILD_RESULT_PENDING,
                                                  TASK_BUILD_RESULT_QUEUE])).all()
        for build_task_run in build_task_run_list:
            try:
                find_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == build_task_run.build_jenkins).first()
                if find_job is None:
                    raise ValueError("not found the jenkins job!")
                if find_job.jenkins_url not in current_app.config["JENKINS_DICT"]:
                    raise ValueError("not found the jenkins url's config!")
                username = current_app.config["JENKINS_DICT"][find_job.jenkins_url]["USER_ID"]
                password = current_app.config["JENKINS_DICT"][find_job.jenkins_url]["USER_PWD"]
                server = jenkins.Jenkins(find_job.jenkins_url,
                                         username=username,
                                         password=password)
                current_app.logger.info("更新构建任务状态，分支：%s，环境：%s" % (
                    build_task_run.build_branch, build_task_run.build_env))
                # 如果是初始化状态，则新建
                if build_task_run.build_result == TASK_BUILD_RESULT_PENDING:
                    build_param = json.loads(build_task_run.build_param)["env"]
                    build_param["branch"] = build_task_run.build_branch
                    build_param["env"] = build_task_run.build_env
                    build_param["test_version"] = build_task_run.build_env
                    # 处理payment的请求环境是test1,test2,test3
                    if len(build_param["test_version"]) > 4 and "test" in build_param["test_version"]:
                        build_param["num"] = build_task_run.build_env[-1]
                    elif build_param["test_version"] == "staging":
                        build_param["num"] = 1
                    elif build_param["test_version"] == "test":
                        build_param["num"] = 2

                    queue_id = server.build_job(build_task_run.build_jenkins, parameters=build_param)
                    build_task_temp = AssumptBuildTask.query.filter(
                        AssumptBuildTask.id == build_task_run.build_task_id).first()
                    build_task_run_temp = AssumptBuildTaskRun.query.filter(
                        AssumptBuildTaskRun.id == build_task_run.id).first()
                    build_task_temp.last_build_status = TASK_BUILD_RESULT_QUEUE
                    build_task_run_temp.build_jenkins_queue_id = queue_id
                    build_task_run_temp.build_result = TASK_BUILD_RESULT_QUEUE
                    db.session.add(build_task_temp)
                    db.session.add(build_task_run_temp)
                    db.session.flush()
                    trigger_build_coverage(build_task_temp)
                    current_app.logger.info("更新构建任务状态，分支：%s，环境：%s，任务：%s，队列id：%s，构建成功" % (
                        build_task_run.build_branch, build_task_run.build_env,
                        build_task_run.build_jenkins, queue_id))
                    continue
                # 如果是排队中，则更新构建序号
                if build_task_run.build_result == TASK_BUILD_RESULT_QUEUE:
                    # 先查询排队信息
                    try:
                        queue_info = server.get_queue_item(build_task_run.build_jenkins_queue_id)
                    except:
                        queue_info = None
                    # 如果已经在构建中了，则更新build_num
                    if queue_info is not None and \
                            queue_info["blocked"] is False and \
                            "executable" in queue_info.keys() and \
                            queue_info["executable"] is not None and \
                            queue_info["task"]["name"] == build_task_run.build_jenkins:
                        build_task = AssumptBuildTask.query.filter(
                            AssumptBuildTask.id == build_task_run.build_task_id).first()
                        build_task.last_build_status = TASK_BUILD_RESULT_BUILDING
                        build_task_run.build_result = TASK_BUILD_RESULT_BUILDING
                        build_task_run.build_jenkins_task_id = queue_info["executable"]["number"]
                        db.session.add(build_task)
                        db.session.add(build_task_run)
                        db.session.flush()
                    # 如果还是在排队中，则下次轮训再查
                    elif queue_info is not None and queue_info["blocked"] is True:
                        current_app.logger.error("更新构建任务状态，分支：%s，环境：%s，任务：%s，队列id：%s，还在排队中" %
                                                 (build_task_run.build_branch, build_task_run.build_env,
                                                  build_task_run.build_jenkins, build_task_run.build_jenkins_queue_id))
                    else:
                        current_app.logger.error("更新构建任务状态，分支：%s，环境：%s，任务：%s，队列id：%s，状态未知" %
                                                 (build_task_run.build_branch, build_task_run.build_env,
                                                  build_task_run.build_jenkins, build_task_run.build_jenkins_queue_id))
                    continue
                # 如果是构建中状态，则查询
                if build_task_run.build_result == TASK_BUILD_RESULT_BUILDING:
                    next_build_num = build_task_run.build_jenkins_task_id
                    # 获取构建信息，并更新状态，这里如果报错，则认为构建任务不存在
                    try:
                        build_info = server.get_build_info(build_task_run.build_jenkins, next_build_num)
                    except:
                        current_app.logger.error("更新构建任务状态，分支：%s，环境：%s，任务：%s，id：%s，构建任务未找到" %
                                                 (build_task_run.build_branch, build_task_run.build_env,
                                                  build_task_run.build_jenkins, next_build_num))
                        continue
                    output = server.get_build_console_output(build_task_run.build_jenkins, next_build_num)
                    save_build_message(build_task_run.id,
                                       build_task_run.build_task_id,
                                       build_number=next_build_num,
                                       url=os.path.join(build_info["url"], "console"),
                                       result=build_info["result"],
                                       message=output)
                    current_app.logger.info("更新构建任务状态，分支：%s，环境：%s，任务：%s，id：%s，状态：%s" % (
                        build_task_run.build_branch, build_task_run.build_env, build_task_run.build_jenkins,
                        next_build_num, build_info["result"]))
                    continue
                if build_task_run.build_result not in (0, 1, 2, 3, 4):
                    send_tv("分支：%s assumpt_build_task_run状态错误，状态：%s" %
                                    (build_task_run.build_branch, build_task_run.build_result))
            except Exception as e:
                send_tv(traceback.format_exc())
                current_app.logger.error(e)
                current_app.logger.error(traceback.format_exc())
    except Exception as e:
        send_tv(traceback.format_exc())
        current_app.logger.error(e)
        current_app.logger.error(traceback.format_exc())


def get_auto_jenkins_server():
    jenkins_url = 'https://jenkins-test.kuainiujinke.com/jenkins/'
    username = current_app.config["JENKINS_DICT"][jenkins_url]["USER_ID"]
    password = current_app.config["JENKINS_DICT"][jenkins_url]["USER_PWD"]
    server = jenkins.Jenkins(jenkins_url,
                             username=username,
                             password=password)
    return server, jenkins_url


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_auto_task(self, task_id, env):
    current_app.logger.info("开始执行自动化脚本")
    try:
        url = ""
        task = AssumptBuildTask.query.filter(AssumptBuildTask.id == task_id).first()
        key_value = KeyValue.query.filter(KeyValue.key == 'auto_jenkins').first()
        if not key_value:
            raise ValueError("not fount the key-v auto_jenkins found!")
        if not task:
            raise ValueError("not found the task ")
        jenkins_dict = json.loads(key_value.value)
        server, jenkins_url = get_auto_jenkins_server()
        if task.gitlab_program_name not in jenkins_dict:
            print("not found the gitlab program's  ")
        else:
            jenkins_name = jenkins_dict[task.gitlab_program_name]['name']
            build_param = {
                "test_branch": "master",
                "env": env,
                "case": jenkins_dict[task.gitlab_program_name]['case']
            }
            queue_id = server.build_job(jenkins_name, parameters=build_param)
            task.auto_queue_id = queue_id
            url = "{0}view/auto_test/job/{1}/".format(jenkins_url, jenkins_name)
            try:
                queue_info = server.get_queue_item(task.auto_queue_id)
            except jenkins.JenkinsException:
                pass
            else:
                if queue_info and queue_info["blocked"] is False and "executable" in queue_info.keys() and \
                        queue_info["executable"] is not None and queue_info["task"]["name"] == jenkins_name:
                    next_build_num = queue_info["executable"]["number"]
                    url = "{0}/view/auto_test/job/{1}/{2}/".format(jenkins_url, jenkins_name, next_build_num)
            task.auto_url = url
            db.session.add(task)
            db.session.flush()
            # 如果是初始化状态，则新建
    except Exception as e:
        url = e
        send_tv(traceback.format_exc())
        current_app.logger.error(e)
        current_app.logger.error(traceback.format_exc())
    finally:
        return url


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_run_auto_task(self):
    # 如果已经在构建中了，则更新build_num
    task_list = AssumptBuildTask.query.filter(AssumptBuildTask.auto_queue_id != 0).all()
    if not task_list:
        return
    key_value = KeyValue.query.filter(KeyValue.key == 'auto_jenkins').first()
    if not key_value:
        raise ValueError("not fount the key-v auto_jenkins found!")
    jenkins_dict = json.loads(key_value.value)
    server, jenkins_url = get_auto_jenkins_server()
    for task in task_list:
        if task.gitlab_program_name not in jenkins_dict:
            raise ValueError("not found the gitlab program's  ")
        jenkins_name = jenkins_dict[task.gitlab_program_name]['name']
        if task.auto_url == "{0}view/auto_test/job/{1}/".format(jenkins_url, jenkins_name):
            try:
                queue_info = server.get_queue_item(task.auto_queue_id)
            except jenkins.JenkinsException as e:
                task.auto_url = str(e)
                db.session.add(task)
                continue
            if queue_info and queue_info["blocked"] is False and "executable" in queue_info.keys() and \
                    queue_info["executable"] is not None and queue_info["task"]["name"] == jenkins_name:
                next_build_num = queue_info["executable"]["number"]
                url = "{0}/view/auto_test/job/{1}/{2}/console".format(jenkins_url, jenkins_name, next_build_num)
                task.auto_url = url
                db.session.add(task)
    db.session.flush()


def save_build_message(build_task_run_id, build_task_id, **kwargs):
    next_build_number = kwargs["build_number"]
    url = kwargs["url"]
    result = kwargs["result"]
    build_task_run = AssumptBuildTaskRun.query.filter(AssumptBuildTaskRun.id == build_task_run_id).first()
    build_task = AssumptBuildTask.query.filter(AssumptBuildTask.id == build_task_id).first()
    if build_task and build_task_run:
        # build_task.build_message = message
        # 不保存具体日志信息，改为保存日志链接地址
        build_task_run.build_jenkins_task_id = next_build_number
        build_task_run.build_message = url
        if result in ("ERROR", "FAILURE"):
            build_task_run.build_result = TASK_BUILD_RESULT_FAILED
            build_task.last_build_status = TASK_BUILD_RESULT_FAILED
        elif result == "BUILDING":
            build_task_run.build_result = TASK_BUILD_RESULT_BUILDING
            build_task.last_build_status = TASK_BUILD_RESULT_BUILDING
        elif result == "SUCCESS":
            build_task_run.build_result = TASK_BUILD_RESULT_SUCCESS
            build_task.last_build_status = TASK_BUILD_RESULT_SUCCESS
            # get_pod_str = "kubectl get pod -o wide"
            # if get_pod_str in message:
            #     get_pod_run_str = message.split(get_pod_str)[-1]
            #     if "Running" in get_pod_run_str:
            #         get_pod_id_list = get_pod_run_str.split("Running")[1]
            #         get_pod_id_list = get_pod_id_list.strip().split(" ")
            #         get_pod_id_list = list(filter(lambda x: x, get_pod_id_list))
            #         get_pod_ip = get_pod_id_list[2]
            #         get_pod_env = build_task.last_build_env
            #         find_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == jenkins_job).first()
            #         if find_job is not None and find_job.change_ip:
            #             new_jenkins_job = json.loads(find_job.git_module)
            #             for env, module in new_jenkins_job.items():
            #                 if env == get_pod_env:
            #                     for module_info in module:
            #                         module_info["address"] = get_pod_ip
            #             find_job.git_module = json.dumps(new_jenkins_job)
            #             db.session.add(find_job)
            #     else:
            #         current_app.logger.info("not fount Running in message, build_task is {0}".format(build_task_id))
        elif result == "ABORTED":
            build_task_run.build_result = TASK_BUILD_RESULT_CANCEL
            build_task.last_build_status = TASK_BUILD_RESULT_CANCEL
        else:
            build_task_run.build_result = TASK_BUILD_RESULT_BUILDING
            build_task.last_build_status = TASK_BUILD_RESULT_BUILDING
        db.session.add(build_task_run)
        db.session.add(build_task)
        db.session.flush()
