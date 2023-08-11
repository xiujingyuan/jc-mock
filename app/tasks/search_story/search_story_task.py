#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/09/09
 @file: search_story.py
 @site:
 @email:
"""
import time
import traceback
from datetime import datetime

import requests
from celery_once import QueueOnce

from app import celery
from flask import current_app
import json
from app import db
from app.common.Tapd import get_tapd_story_for_status, get_current_iteration_all, get_build_branch
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from sqlalchemy import and_

from app.models.JenkinsJobDb import JenkinsJob
from app.models.SysProgramDb import SysProgram
from app.tools.tools import send_tv


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_for_test(self):
    date_start = datetime.now()
    current_app.logger.info("定时任务-检查需求状态-开始！")
    sys_programs = SysProgram.serialize_list(SysProgram.query.filter().all())
    for program in sys_programs:
        current_app.logger.info("定时任务-检查需求状态-项目：{0}, work_id is:{1} ！".format(
            program["sys_program_desc"],
            program["tapd_work_ids"]))
        if program["tapd_work_ids"] is not None and len(program["tapd_work_ids"]) > 0:
            date1 = datetime.now()
            for work_id in program["tapd_work_ids"]:
                status = ["for_test", "testing"] if work_id != 59247418 else ['status_4', 'status_5']
                stories = get_tapd_story_for_status(work_id, status=status)
                for story in stories:
                    build_branch_infos = get_build_branch(program["sys_program_desc"],
                                                          story["Story"]["id"][-7:])["data"]
                    for build_branch_info in build_branch_infos:
                        if build_branch_info["branch"] == 'master':
                            search_task = AssumptBuildTask.query.filter(and_(
                                AssumptBuildTask.program_id == program["sys_program_id"],
                                AssumptBuildTask.work_id == work_id,
                                AssumptBuildTask.story_full_id == story["Story"]["id"])).first()
                        else:
                            search_task = AssumptBuildTask.query.filter(and_(
                                AssumptBuildTask.program_id == program["sys_program_id"],
                                AssumptBuildTask.work_id == work_id,
                                AssumptBuildTask.story_full_id == story["Story"]["id"],
                                AssumptBuildTask.gitlab_program_id == build_branch_info["program"])).first()
                        if search_task is None:
                            jenkins_job = JenkinsJob.query.filter(
                                JenkinsJob.gitlab_program_id == build_branch_info["program"]).first()
                            new_task = AssumptBuildTask()
                            new_task.iteration_id = ''
                            new_task.story_full_id = story["Story"]["id"]
                            new_task.story_id = story["Story"]["id"][-7:]
                            new_task.story_url = "https://www.tapd.cn/{1}/prong/stories/view/{0}".format(
                                story["Story"]["id"], work_id)
                            new_task.story_name = story["Story"]["name"]
                            new_task.work_id = work_id
                            new_task.program_id = program["sys_program_id"]
                            new_task.program_name = program["sys_program_desc"]
                            new_task.gitlab_program_id = build_branch_info["program"]
                            new_task.build_branch = build_branch_info["branch"]
                            new_task.mail_receive_time = story["Story"]["modified"]

                            # 通过获取的gitlab的ID来查找
                            new_task.build_jenkins_jobs = ""
                            new_task.filter_file_value = json.dumps({"exclude": "test"})
                            new_task.gitlab_program_name = ""\
                                if jenkins_job is None else jenkins_job.service_name
                            db.session.add(new_task)
                            db.session.flush()
                            # 持续集成，提测后对相应分支进行测试
                            try:
                                url = "https://k8s-test-rancher.kuainiujinke.com/ci/hook_api"
                                body = {"ref": build_branch_info["branch"],
                                        "user_name": "test_platform",
                                        "project": {"id": build_branch_info["program"]}}
                                header = {"X-Gitlab-Event": "Submit Hook", "Content-Type": "application/json"}
                                requests.post(url=url, json=body, headers=header)
                            except Exception as e:
                                send_tv("持续集成报错：%s" % str(e))
                                current_app.logger.info(traceback.format_exc())
                                pass
            current_app.logger.info("定时任务-检查需求状态-项目：{0}, work_id is:{1}, 耗时{2}".format(
                program["sys_program_desc"],
                program["tapd_work_ids"],
                (datetime.now() - date1).seconds))
    current_app.logger.info("定时任务-检查需求状态-结束！耗时%s" % (datetime.now() - date_start).seconds)
