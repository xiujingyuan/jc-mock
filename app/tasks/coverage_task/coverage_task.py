#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/04
 @file: coverage_task.py
 @site:
 @email:
"""

import json
import time
import traceback
from datetime import datetime

from celery_once import QueueOnce

from app import db
from flask import current_app
from app import celery
import requests
from sqlalchemy import and_
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.CoverageInfoDb import CoverageInfo
from app.models.JenkinsJobDb import JenkinsJob
from app.models.TestEnvDb import TestEnv
from app.tools.tools import send_tv


CONTENT_DEFAULT = {
    "detailInfo": [],
    "basicInfo": {
        "coverage": "0%",
        "total": "0",
        "missing": "0"
    }
}


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_diff_coverage_new(self):
    """
    根据分支，等获取增量覆盖率
    :return:
    """
    branch = ""
    date_start = datetime.now()
    current_app.logger.info("获取增量覆盖率任务开始！")
    diff_task_list = AssumptBuildTask.query.filter(AssumptBuildTask.build_task_status == 1,
                                                   AssumptBuildTask.build_count > 0).all()
    for diff_task in diff_task_list:
        try:
            branch = diff_task.build_branch
            # 分支未获取到，不去获取覆盖率
            if branch == 'not found' or branch == "master":
                continue

            # 不需要获取覆盖率的分支
            jenkins_job_list = JenkinsJob.query.filter(
                JenkinsJob.gitlab_program_id == diff_task.gitlab_program_id,
                JenkinsJob.is_collect == 1).all()
            current_app.logger.info("获取增量覆盖率-开始！ 分支：%s" % branch)
            for jenkins_info in jenkins_job_list:
                if jenkins_info is None or jenkins_info.git_module is None or len(jenkins_info.git_module) == 0:
                    current_app.logger.info("not found the env info!")
                    continue

                env_list = TestEnv.query.filter(TestEnv.service_names == jenkins_info.service_name).all()
                env_id_list = [env.env_id for env in env_list]
                current_app.logger.info("获取增量覆盖率-开始！分支：{0} 系统：{1}  环境：{2}".format(branch, jenkins_info.service_name, env_id_list))
                for env in env_list:
                    uuid = jenkins_info.service_name + "_" + diff_task.build_branch + "_" + env.env_id
                    result = requests.get(
                        current_app.config["JENKINS_DICT"][jenkins_info.jenkins_url]["SUPER_JACOCO"] +
                        current_app.config["SUPER_JACOCO_GET"] + "?uuid=" + uuid)
                    result = result.json()
                    if int(result["data"]["coverStatus"]) == 1:
                        save_coverage_info_new(jenkins_info, diff_task.build_branch, env.env_id, result["data"])
                        # 这里需要更新assumpt_build_task里的覆盖率，需要和表里的服务名环境一致
                        if jenkins_info.service_name == diff_task.gitlab_program_name and \
                                str(env.env_id) == str(diff_task.last_build_env):
                            diff_task.last_coverage = result["data"]["lineCoverage"]
                            db.session.add(diff_task)
                            db.session.flush()
            current_app.logger.info("获取增量覆盖率-结束！分支：{0}".format(branch))
        except:
            send_tv(traceback.format_exc())
            current_app.logger.error(traceback.format_exc())
            current_app.logger.info("获取增量覆盖率-异常！分支：{0}".format(branch))
            continue
    current_app.logger.info("获取增量覆盖率-完成！耗时%s" % (datetime.now() - date_start).seconds)


def trigger_build_coverage(build_task):
    """
    根据分支，开始构建增量覆盖率
    """
    current_app.logger.info("构建增量覆盖率任务开始！")
    env_id = build_task.last_build_env
    branch = build_task.build_branch
    system = build_task.gitlab_program_name
    try:
        job_info = JenkinsJob.query.filter(and_(JenkinsJob.jenkins_job_name == build_task.build_jenkins_jobs,
                                                JenkinsJob.is_active == 1,
                                                JenkinsJob.is_collect == 1)).first()
        if job_info is not None and job_info.git_module is not None and len(job_info.git_module) > 0 and env_id in json.loads(
                job_info.git_module):
            if "master" not in branch and branch != "not found":
                module_info = json.loads(job_info.git_module)[env_id][0]
                try:
                    filter_file = json.loads(build_task.filter_file_value)
                    if len(filter_file["exclude"]) > 0:
                        filter_file = filter_file["exclude"]
                    else:
                        filter_file = "test"
                except:
                    filter_file = "test"
                super_jacoco_data = {
                    "uuid": job_info.service_name + "_" + branch + "_" + env_id,
                    "type": 2,
                    "gitUrl": job_info.gitlab_program_http_url,
                    "subModule": "",
                    "baseVersion": "master",
                    "nowVersion": branch,
                    "address": module_info["address"],
                    "port": module_info["port"],
                    "exclude": filter_file if filter_file is not None and len(filter_file) > 0 else "test",
                    "mvnExtend": job_info.mvn_extend,
                    "mvnVersion": job_info.mvn_version
                }
                requests.post(current_app.config["JENKINS_DICT"][job_info.jenkins_url]["SUPER_JACOCO"] +
                              current_app.config["SUPER_JACOCO_TRIGGER"], json=super_jacoco_data)
    except:
        send_tv("构建增量覆盖率报错%s" % traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
        current_app.logger.info("构建增量覆盖率-异常！系统：{0} 分支：{1} 环境：{2}".format(system, branch, env_id))
    else:
        current_app.logger.info("构建增量覆盖率-结束！系统：{0} 分支：{1} 环境：{2}".format(system, branch, env_id))


def save_coverage_info_new(jenkins, branch, env, result):
    coverage_info = CoverageInfo.query.filter(and_(
        CoverageInfo.service_name == jenkins.service_name,
        CoverageInfo.env == env,
        CoverageInfo.compare_branch == branch,
        CoverageInfo.new_coverage == 1)).order_by(
        CoverageInfo.version.desc()).first()
    if coverage_info:
        coverage_result = json.loads(coverage_info.content)
        if float(coverage_result["lineCoverage"]) == float(result["lineCoverage"]):
            coverage_info.content = json.dumps(result, ensure_ascii=False)
            coverage_info.update_time = datetime.now()
        else:
            coverage_info = CoverageInfo()
            coverage_info.compare_branch = branch
            coverage_info.service_name = jenkins.service_name,
            coverage_info.branch = result["nowCommitId"]
            coverage_info.env = env
            coverage_info.gitlab_program_id = jenkins.gitlab_program_id
            coverage_info.content = json.dumps(result, ensure_ascii=False)
            coverage_info.line_coverage = float(result["lineCoverage"])
            coverage_info.coverage_url = result["reportUrl"]
            coverage_info.version = int(time.time())
            coverage_info.update_time = datetime.now()
            coverage_info.new_coverage = 1
    else:
        coverage_info = CoverageInfo()
        coverage_info.compare_branch = branch
        coverage_info.service_name = jenkins.service_name
        coverage_info.branch = result["nowCommitId"]
        coverage_info.env = env
        coverage_info.gitlab_program_id = jenkins.gitlab_program_id
        coverage_info.content = json.dumps(result, ensure_ascii=False)
        coverage_info.line_coverage = float(result["lineCoverage"])
        coverage_info.coverage_url = result["reportUrl"]
        coverage_info.version = int(time.time())
        coverage_info.update_time = datetime.now()
        coverage_info.new_coverage = 1
    db.session.add(coverage_info)
    db.session.flush()
