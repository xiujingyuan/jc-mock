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
import re
import time
import traceback
from datetime import datetime

import gitlab
import requests
from celery_once import QueueOnce
from dateutil.relativedelta import relativedelta

from app import db
from flask import current_app
from app import celery
from sqlalchemy import and_

from app.common.Tapd import get_tapd_map, get_tapd_story, get_tapd_bug, get_tapd_api, \
    get_tapd_case, get_tapd_test_plan, get_relations_by_story, get_special_status_story_completed_time
from app.models.GitMergeInfoDb import GitMergeInfo
from app.models.SonarInfoDb import SonarInfo
from app.models.SysProgramDb import SysProgram
from app.models.TapdBugDetailDb import TapdBugDetail
from app.models.TapdCaseDetailDb import TapdCaseDetail
from app.models.TapdKeyValueDb import TapdKeyValue
from app.models.TapdStoryDetailDb import TapdStoryDetail
from app.models.GitTagInfoDb import GitTagInfo
from app.models.TapdTestPlanDetailDb import TapdTestPlanDetail
from app.tools.tools import send_tv


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_story_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取测试本月的需求和bug数据
    :return:
    """
    current_app.logger.info("获取本月的需求数据开始！")
    date_start = datetime.now()
    search_programs = db.session.query(SysProgram).filter(and_(SysProgram.tapd_work_ids != "")).all()
    query_start_time = get_date(month=-int(query_month), fmt="%Y-%m-%d") if query_start_time is None else \
        datetime.strptime(query_start_time, '%Y-%m-%d')
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            for work_id in json.loads(program.tapd_work_ids):
                stories = get_tapd_story(work_id, query_start_time=query_start_time)
                for story in stories:
                    story_id = story["Story"]["id"]
                    search_story = db.session.query(TapdStoryDetail).filter(
                        TapdStoryDetail.story_id == story_id).first()
                    if search_story is None:
                        search_story = TapdStoryDetail()
                    search_story.story_id = story["Story"]["id"]
                    search_story.story_name = story["Story"]["name"]
                    search_story.story_workspace_id = work_id
                    search_story.story_iteration_id = story["Story"]["iteration_id"]
                    search_story.story_create = story["Story"]["created"]
                    search_story.story_create_date = story["Story"]["created"].split(" ")[0]
                    search_story.story_completed = story["Story"]["completed"]
                    search_story.story_status = story["Story"]["status"]
                    search_story.story_category = get_story_category(work_id, story)
                    search_story.story_tester = get_story_tester(work_id, story)
                    search_story.story_developer = story["Story"]["developer"]
                    search_story.story_url = "https://www.tapd.cn/{0}/prong/stories/view/{1}".format(
                        work_id,
                        story["Story"]["id"]
                    )
                    search_story.is_effective = 1
                    if program.sys_program_id == 24 and story["Story"]["status"] == "status_1":
                        search_story.story_completed = get_special_status_story_completed_time(work_id,
                                                                                               story["Story"]["id"])
                    db.session.add(search_story)
                    db.session.flush()
            current_app.logger.info("获取本月的需求数据-完成！项目：{0}".format(program.sys_program_id))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取本月的需求数据-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取本月的需求数据-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
        send_tv("获取本月的需求数据，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取本月的需求数据结束！")
    send_tv("获取本月的需求数据，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_test_plan_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取测试本月的计划数据
    :return:
    """
    current_app.logger.info("获取本月的测试计划数据开始！")
    date_start = datetime.now()
    search_programs = db.session.query(SysProgram).filter(and_(SysProgram.tapd_work_ids != "")).all()
    query_start_time = get_date(month=-int(query_month), fmt="%Y-%m-%d") if query_start_time is None else \
        datetime.strptime(query_start_time, '%Y-%m-%d')
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            for work_id in json.loads(program.tapd_work_ids):
                test_plans = get_tapd_test_plan(work_id, query_start_time=query_start_time)
                for plan in test_plans:
                    plan_id = plan["TestPlan"]["id"]
                    search_plan = db.session.query(TapdTestPlanDetail).filter(TapdTestPlanDetail.test_plan_id ==
                                                                              plan_id).first()
                    if search_plan is None:
                        new_plan = TapdTestPlanDetail()
                        new_plan.test_plan_id = plan["TestPlan"]["id"]
                        new_plan.test_plan_name = plan["TestPlan"]["name"]
                        new_plan.test_plan_workspace_id = work_id
                        new_plan.test_plan_iteration_id = ""
                        new_plan.test_plan_story_id = ""
                        new_plan.test_plan_create = plan["TestPlan"]["created"]
                        new_plan.test_plan_create_date = plan["TestPlan"]["created"].split(" ")[0]
                        new_plan.test_plan_status = plan["TestPlan"]["status"]
                        new_plan.test_plan_url = "https://www.tapd.cn/{0}/sparrow/test_plan/view/{1}".format(
                            work_id,
                            plan["TestPlan"]["id"]
                        )
                        db.session.add(new_plan)
                        db.session.flush()
                    else:
                        search_plan.test_plan_name = plan["TestPlan"]["name"]
                        search_plan.test_plan_status = plan["TestPlan"]["status"]
                        db.session.add(search_plan)
                        db.session.flush()
            current_app.logger.info("获取本月的测试计划数据-完成！项目：{0}".format(program.sys_program_id))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取本月的测试计划数据-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取本月的测试计划数据-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
        send_tv("获取本月的测试计划数据，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取本月的测试计划数据结束！")
    send_tv("获取本月的测试计划数据，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_case_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取测试本月的用例数据
    :return:
    """
    current_app.logger.info("获取本月的测试用例数据开始！")
    date_start = datetime.now()
    search_programs = db.session.query(SysProgram).filter(and_(SysProgram.tapd_work_ids != "")).all()
    query_start_time = get_date(month=-int(query_month), fmt="%Y-%m-%d") if query_start_time is None else \
        datetime.strptime(query_start_time, '%Y-%m-%d')
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            for work_id in json.loads(program.tapd_work_ids):
                cases = get_tapd_case(work_id, query_start_time=query_start_time)
                for case in cases:
                    search_case = db.session.query(TapdCaseDetail).filter(
                        TapdCaseDetail.case_id == case["Tcase"]["id"]).first()
                    if search_case is None:
                        new_case = TapdCaseDetail()
                        new_case.case_id = case["Tcase"]["id"]
                        new_case.case_name = case["Tcase"]["name"]
                        new_case.case_workspace_id = work_id
                        new_case.case_iteration_id = ""
                        new_case.case_story_id = ""
                        new_case.case_create = case["Tcase"]["created"]
                        new_case.case_create_date = case["Tcase"]["created"].split(" ")[0]
                        new_case.case_precondition = case["Tcase"]["precondition"]
                        new_case.case_steps = case["Tcase"]["steps"]
                        new_case.case_expectation = case["Tcase"]["expectation"]
                        new_case.case_status = case["Tcase"]["status"]
                        new_case.case_priority = case["Tcase"]["priority"]
                        new_case.case_type = case["Tcase"]["type"]
                        new_case.case_url = "https://www.tapd.cn/{0}/sparrow/tcase/view/{1}".format(
                            work_id,
                            case["Tcase"]["id"]
                        )
                        new_case.case_category_id = case["Tcase"]["category_id"]
                        new_case.case_creator = case["Tcase"]["creator"]
                        db.session.add(new_case)
                        db.session.flush()
            current_app.logger.info("获取本月的测试用例数据-完成！项目：{0}".format(program.sys_program_id))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取本月的测试用例数据-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取本月的测试用例数据-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
        send_tv("获取本月的测试用例数据，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取本月的测试用例数据结束！")
    send_tv("获取本月的测试用例数据，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_bug_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取测试本月的需求和bug数据
    :return:
    """
    current_app.logger.info("获取本月的bug数据开始！")
    date_start = datetime.now()
    search_programs = db.session.query(SysProgram).filter(and_(SysProgram.tapd_work_ids != "")).all()
    query_start_time = get_date(month=-int(query_month), fmt="%Y-%m-%d") if query_start_time is None else \
        datetime.strptime(query_start_time, '%Y-%m-%d')
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            for work_id in json.loads(program.tapd_work_ids):
                bugs = get_tapd_bug(work_id, query_start_time=query_start_time)
                for bug in bugs:
                    search_bug = db.session.query(TapdBugDetail).filter(
                        TapdBugDetail.bug_id == bug["Bug"]["id"]).first()
                    if search_bug is None:
                        search_bug = TapdBugDetail()
                        search_bug.bug_id = bug["Bug"]["id"]
                        search_bug.bug_name = bug["Bug"]["title"]
                        search_bug.bug_workspace_id = work_id
                        search_bug.bug_iteration_id = bug["Bug"]["iteration_id"]
                        search_bug.bug_story_id = ""
                        search_bug.bug_create = bug["Bug"]["created"]
                        search_bug.bug_create_date = bug["Bug"]["created"].split(" ")[0]
                        search_bug.bug_status = bug["Bug"]["status"]
                        search_bug.bug_severity = bug["Bug"]["severity"]
                        search_bug.bug_dev = bug["Bug"]["de"]
                        search_bug.bug_tester = bug["Bug"]["te"]
                        search_bug.source = bug["Bug"]["source"]
                        search_bug.reject_time = bug["Bug"]["reject_time"]
                        search_bug.reopen_time = bug["Bug"]["reopen_time"]
                        if re.match(r".*(online|Online).*", bug["Bug"]["title"].lower()) or \
                                re.match(r".*(online|Online).*", bug["Bug"]["version_report"].lower()):
                            bug["Bug"]["version_report"] = 'online_bug'
                        search_bug.find_version = bug["Bug"]["version_report"]
                        search_bug.bug_url = "https://www.tapd.cn/{0}/bugtrace/bugs/view?bug_id={1}".format(
                            work_id,
                            bug["Bug"]["id"]
                        )
                        db.session.add(search_bug)
                        db.session.flush()
                    else:
                        search_bug.bug_name = bug["Bug"]["title"]
                        search_bug.bug_iteration_id = bug["Bug"]["iteration_id"]
                        search_bug.bug_status = bug["Bug"]["status"]
                        search_bug.bug_severity = bug["Bug"]["severity"]
                        search_bug.bug_dev = bug["Bug"]["de"]
                        search_bug.bug_tester = bug["Bug"]["te"]
                        search_bug.source = bug["Bug"]["source"]
                        search_bug.reject_time = bug["Bug"]["reject_time"]
                        search_bug.reopen_time = bug["Bug"]["reopen_time"]
                        if re.match(r".*(online|Online).*", bug["Bug"]["title"].lower()) or \
                                re.match(r".*(online|Online).*", bug["Bug"]["version_report"].lower()):
                            bug["Bug"]["version_report"] = 'online_bug'
                        search_bug.find_version = bug["Bug"]["version_report"]
                        if program.sys_program_group_id == 10 and bug["Bug"]["custom_field_one"] is not None:
                            search_bug.find_version = bug["Bug"]["custom_field_one"]
                        db.session.add(search_bug)
                        db.session.flush()
            current_app.logger.info("获取本月的bug数据-完成！项目：{0}".format(program.sys_program_id))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取本月的bug数据-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取本月的bug数据-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
        send_tv("获取本月的bug数据，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取本月的bug数据结束！")
    send_tv("获取本月的bug数据，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_relation_data(self):
    """
    获取测试本月的需求和bug数据
    :return:
    """
    current_app.logger.info("获取所有需求关联的用例和测试计划开始！")
    search_programs = db.session.query(SysProgram).filter(and_(
        SysProgram.tapd_work_ids != "")).all()
    for program in search_programs:
        try:
            for work_id in json.loads(program.tapd_work_ids):
                storys = TapdStoryDetail.query.filter(TapdStoryDetail.story_workspace_id == work_id).all()
                for story in storys:
                    relations = get_relations_by_story(work_id, story.story_id)
                    for relation in relations:
                        if relation["TestPlanStoryTcaseRelation"]["story_id"] == story.story_id and \
                                int(relation["TestPlanStoryTcaseRelation"]["test_plan_id"]) != 0 and \
                                story.story_iteration_id != 0:
                            db.session.execute("update tapd_test_plan_detail "
                                               "set test_plan_iteration_id='%s', test_plan_story_id='%s' "
                                               "where test_plan_id='%s'" % (
                                                   story.story_iteration_id,
                                                   story.story_id,
                                                   relation["TestPlanStoryTcaseRelation"]["test_plan_id"]))
                        if relation["TestPlanStoryTcaseRelation"]["story_id"] == story.story_id and \
                                int(relation["TestPlanStoryTcaseRelation"]["tcase_id"]) != 0 and \
                                story.story_iteration_id != 0:
                            db.session.execute("update tapd_case_detail "
                                               "set case_iteration_id='%s', case_story_id='%s' "
                                               "where case_id='%s'" % (
                                                   story.story_iteration_id,
                                                   story.story_id,
                                                   relation["TestPlanStoryTcaseRelation"]["tcase_id"]))
                    time.sleep(1)

            current_app.logger.info("获取所有需求关联的用例和测试计划-完成！项目：{0}".format(program.sys_program_id))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取所有需求关联的用例和测试计划-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取所有需求关联的用例和测试计划-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
    current_app.logger.info("获取所有需求关联的用例和测试计划结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_git_merge_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取测试本月的项目对应分支的代码提交情况
    :return:
    """
    current_app.logger.info("获取项目对应分支的代码merge情况开始！")
    date_start = datetime.now()
    if query_start_time is None:
        query_start_time = get_date(month=-int(query_month))
    search_programs = db.session.query(SysProgram).filter(SysProgram.git_program_ids != "").all()
    gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
    gl.auth()
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            git_program_ids = json.loads(program.git_program_ids)
            for git_program_name, git_program_id in git_program_ids.items():
                git_project = gl.projects.get(git_program_id)
                merge_list = git_project.mergerequests.list(
                    updated_after=query_start_time, state='merged', order_by='updated_at', all=True)
                for merge in merge_list:
                    merge_info = GitMergeInfo.query.filter(GitMergeInfo.merge_id == merge.attributes["id"]).first()
                    if merge_info is not None:
                        pass
                    else:
                        merge_info = GitMergeInfo()
                    commit_info = git_project.commits.get(merge.attributes["merge_commit_sha"]).attributes
                    try:
                        diffs = git_project.repository_compare(merge.diffs.list()[0].attributes["start_commit_sha"],
                                                               merge.attributes["merge_commit_sha"])
                    except:
                        diffs = None
                    created_time = merge.attributes["merged_at"][:-5] \
                        if merge.attributes["merged_at"] is not None \
                        else merge.attributes["updated_at"][:-5]
                    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S')
                    merge_info.merge_id = merge.attributes["id"]
                    merge_info.merge_title = merge.attributes["title"]
                    merge_info.source_branch = merge.attributes["source_branch"] \
                        if merge.attributes["source_branch"].startswith("origin") is False \
                        else merge.attributes["source_branch"].split("/")[1]
                    merge_info.target_branch = merge.attributes["target_branch"]
                    merge_info.start_commit_sha = merge.diffs.list()[0].attributes["start_commit_sha"]
                    merge_info.end_commit_sha = merge.attributes["merge_commit_sha"]
                    merge_info.merge_create_user = merge.attributes["author"]["name"]
                    merge_info.merge_close_user = merge.attributes["merged_by"]["name"]
                    merge_info.merge_create_date = created_time.date()
                    merge_info.merge_create = created_time
                    merge_info.git_add_lines = commit_info["stats"]["additions"]
                    merge_info.git_remove_lines = commit_info["stats"]["deletions"]
                    merge_info.git_commit_count = len(diffs["commits"]) if diffs is not None else 0
                    merge_info.git_changed_file = len(diffs["diffs"]) if diffs is not None else 0
                    merge_info.gitlab_id = git_program_id
                    merge_info.gitlab_name = git_program_name
                    db.session.add(merge_info)
                    db.session.flush()
                current_app.logger.info(
                    "获取项目对应分支的代码merge情况，完成！系统：%s 项目：%s " % (program.sys_program_name, git_program_name))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取项目对应分支的代码merge情况-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取项目对应分支的代码merge情况-异常！堆栈：{0}".format(traceback.format_exc()))
        send_tv("获取项目对应分支的代码merge情况，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取项目对应分支的代码merge情况结束！")
    send_tv("获取项目对应分支的代码merge情况，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_git_tag_data(self, program_id=None, query_start_time=None, query_month=1):
    """
    获取项目本月的上线数据
    :return:
    """
    current_app.logger.info("获取项目本月的上线数据开始！")
    date_start = datetime.now()
    if query_start_time is None:
        query_start_time = get_date(month=-int(query_month))
    search_programs = db.session.query(SysProgram).filter(SysProgram.git_program_ids != "").all()
    gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
    gl.auth()
    for program in search_programs:
        date1 = datetime.now()
        try:
            if program_id is not None and program_id == 0:
                pass
            elif program_id is not None and program_id != 0 and program_id != program.sys_program_id:
                continue
            git_program_ids = json.loads(program.git_program_ids)
            for git_program_name, git_program_id in git_program_ids.items():
                git_project = gl.projects.get(git_program_id)
                tag_list = git_project.tags.list(since=query_start_time, all=True)
                for tag in tag_list:
                    new_tag = db.session.query(GitTagInfo).filter(and_(
                        GitTagInfo.tag_id == tag.target,
                        GitTagInfo.tag_commit_id == tag.commit["id"])).first()
                    if new_tag is None:
                        new_tag = GitTagInfo()
                    if tag.commit["committed_date"].endswith("08:00"):
                        new_tag_time = datetime.strptime(tag.commit["committed_date"], '%Y-%m-%dT%H:%M:%S.000+08:00')
                    else:
                        new_tag_time = datetime.strptime(tag.commit["committed_date"], '%Y-%m-%dT%H:%M:%S.000+00:00')
                    new_tag.tag_id = tag.target
                    new_tag.tag_name = tag.name
                    new_tag.tag_gitlab_id = git_program_id
                    new_tag.tag_create = new_tag_time
                    new_tag.tag_create_date = new_tag_time.date()
                    new_tag.tag_message = tag.message
                    new_tag.tag_commit_id = tag.commit["id"]
                    new_tag.tag_commit_message = tag.commit["message"]
                    db.session.add(new_tag)
                    db.session.flush()
                current_app.logger.info("获取项目本月的上线数据-完成！系统：%s 项目：%s " % (program.sys_program_name, git_program_name))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取项目本月的上线数据-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取项目本月的上线数据-异常！堆栈：{0}".format(traceback.format_exc()))
        send_tv("获取项目本月的上线数据，项目：%s，耗时：%s" % (program.sys_program_name, (datetime.now() - date1).seconds))
    current_app.logger.info("获取项目本月的上线数据结束！")
    send_tv("获取项目本月的上线数据，总耗时：%s" % (datetime.now() - date_start).seconds)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_sonar_data(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目sonar信息开始！")

    all_programs = db.session.query(SysProgram).filter(SysProgram.sys_sonar_key != "").all()
    for program in all_programs:
        try:
            sonar_key = json.loads(program.sys_sonar_key)
            for project_name, project_key in sonar_key.items():
                def get_data(data_json, date_key):
                    ret = {}
                    for mersure in data_json['measures']:
                        key = mersure['metric']
                        for data in mersure['history']:
                            if data['date'] == date_key and 'value' in data.keys():
                                value = data['value']
                                ret[key] = value
                                break
                    return ret

                sonar_base_url = "https://sonar.kuainiujinke.com"
                auth = "b551aa46a348f2f57ef3f7a91916bdbe942b8ca5", ""
                project_analyses_url = sonar_base_url + '/api/project_analyses/search?project=%s&p=1&ps=500' % project_key
                project_analyses_list = json.loads(requests.get(url=project_analyses_url, auth=auth).content)
                if "analyses" not in project_analyses_list.keys():
                    continue
                project_data_url = sonar_base_url + '/api/measures/search_history?component=%s&metrics=bugs,' \
                                                    'code_smells,vulnerabilities,reliability_rating,security_rating,' \
                                                    'sqale_index,sqale_rating,lines_to_cover,uncovered_lines,' \
                                                    'coverage,ncloc,duplicated_lines,duplicated_lines_density,' \
                                                    'duplicated_blocks&ps=1000' % project_key
                project_data_list = json.loads(requests.get(url=project_data_url, auth=auth).content)

                result = {}
                for project_analyses in project_analyses_list['analyses']:
                    project_version = project_analyses["projectVersion"]
                    if project_version not in result.keys():
                        result[project_version] = {}
                    key = project_analyses["key"]
                    date_str = project_analyses["date"]
                    if date_str.endswith("0000"):
                        date = datetime.strptime(project_analyses["date"][:-5],
                                                 '%Y-%m-%dT%H:%M:%S') + relativedelta(hours=8)
                    else:
                        date = datetime.strptime(project_analyses["date"][:-5], '%Y-%m-%dT%H:%M:%S')
                    if key not in result[project_version].keys():
                        result[project_version][key] = {}
                    result[project_version][key]["date"] = date
                    result[project_version][key]["data"] = get_data(project_data_list, date_str)

                for branch, key_list in result.items():
                    for key, data in key_list.items():
                        search_sonar = db.session.query(SonarInfo).filter(SonarInfo.sonar_key == key).first()
                        if search_sonar is None:
                            search_sonar = SonarInfo()
                        else:
                            continue
                        search_sonar.sonar_program_key = project_key
                        search_sonar.sonar_program_name = project_name
                        search_sonar.sonar_branch = branch
                        search_sonar.sonar_key = key
                        search_sonar.sonar_branch_year = data["date"].year
                        search_sonar.sonar_branch_month = data["date"].month
                        search_sonar.sonar_req = str(data)

                        search_sonar.sonar_branch_time = data["date"]
                        for item_key, item_value in data["data"].items():
                            if hasattr(search_sonar, "sonar_" + item_key):
                                setattr(search_sonar, "sonar_" + item_key, item_value)
                        db.session.add(search_sonar)
                        db.session.flush()
                current_app.logger.info("获取项目sonar信息-完成！系统：%s 项目：%s " % (program.sys_program_name, project_name))
        except Exception as e:
            current_app.logger.info(e)
            send_tv("获取项目sonar信息-异常！项目：{0}".format(program.sys_program_id))
            send_tv("获取项目sonar信息-异常！堆栈：{0}".format(traceback.format_exc()))
            continue
    current_app.logger.info("获取项目sonar信息结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_bug_map(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目BUG状态对应的map值开始！")
    try:
        get_tapd_map_task("bug")

    except Exception as e:
        current_app.logger.info(e)
        current_app.logger.info(traceback.format_exc())

        current_app.logger.info("获取项目BUG状态对应的map值-异常！")
    finally:
        current_app.logger.info("获取项目BUG状态对应的map值结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_story_map(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目需求状态对应的map值开始！")
    try:
        get_tapd_map_task("story")

    except Exception as e:
        current_app.logger.info(e)
        current_app.logger.info(traceback.format_exc())

        current_app.logger.info("获取项目需求状态对应的map值-异常！")
    finally:
        current_app.logger.info("获取项目需求状态对应的map值结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_story_fields_info(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目需求自定义字段的map值开始！")
    try:
        get_tapd_map_task("story_fields_info")
    except Exception as e:
        current_app.logger.info(e)
        current_app.logger.info(traceback.format_exc())

        current_app.logger.info("获取项目需求自定义字段的map值-异常！")
    finally:
        current_app.logger.info("获取项目需求自定义字段的map值结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_iteration_map(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目迭代ID对应的名称开始！")
    try:
        get_tapd_map_task("iteration")

    except Exception as e:
        current_app.logger.info(e)
        current_app.logger.info(traceback.format_exc())

        current_app.logger.info("获取项目迭代ID对应的名称-异常！")
    finally:
        current_app.logger.info("获取项目迭代ID对应的名称结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_iteration_data(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目迭代信息-开始！")

    task_type = "iteration"
    search_programs = db.session.query(SysProgram).filter(SysProgram.tapd_work_ids != "").all()
    work_item = {}
    for program in search_programs:
        try:
            for work_id in json.loads(program.tapd_work_ids):
                url = "iterations/?workspace_id={0}".format(work_id)
                tapd_ret = get_tapd_api(url)
                work_item[work_id] = []
                for ret in tapd_ret["data"]:
                    if ret["Iteration"]["status"] == "open":
                        work_item[work_id].append(ret["Iteration"])
                search_key = db.session.query(TapdKeyValue).filter(and_(TapdKeyValue.workspace_id == work_id,
                                                                        TapdKeyValue.type == task_type,
                                                                        TapdKeyValue.key == "tapd_info")).first()
                if search_key is None:
                    search_key = TapdKeyValue()
                    search_key.key = "tapd_info"
                    search_key.old_value = ""
                    search_key.value = json.dumps(work_item[work_id], ensure_ascii=False)
                    search_key.type = task_type
                    search_key.workspace_id = work_id
                    db.session.add(search_key)
                    db.session.flush()
                elif work_item[work_id] and (not search_key.value or (
                        search_key.value and json.loads(search_key.value) != work_item[work_id])):
                    search_key.old_value = search_key.value
                    search_key.value = json.dumps(work_item[work_id], ensure_ascii=False)
                    db.session.add(search_key)
                    db.session.flush()
            current_app.logger.info("获取项目迭代信息-完成！项目:{0}".format(program.sys_program_id))
        except:
            current_app.logger.info(traceback.format_exc())

            current_app.logger.info("获取项目迭代信息-异常！项目:{0}".format(program.sys_program_id))
            continue
    current_app.logger.info("获取项目迭代信息-结束！")


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def get_workspace_info(self):
    """

    :param self:
    :return:
    """
    current_app.logger.info("获取项目命名空间开始！")
    try:
        work_id = 20003261
        task_type = "workspace"
        ret = get_tapd_map(work_id, map_type=task_type)
        search_key = db.session.query(TapdKeyValue).filter(and_(TapdKeyValue.workspace_id == work_id,
                                                                TapdKeyValue.type == task_type,
                                                                TapdKeyValue.key == "tapd_map")).first()
        if search_key is None:
            search_key = TapdKeyValue()
            search_key.key = "tapd_map"
            search_key.old_value = ""
            search_key.value = json.dumps(ret, ensure_ascii=False)
            search_key.type = task_type
            search_key.workspace_id = work_id
            db.session.add(search_key)
            db.session.flush()
        elif not search_key.value or (search_key.value and json.loads(search_key.value) != ret):
            search_key.old_value = search_key.value
            search_key.value = json.dumps(ret, ensure_ascii=False)
            db.session.add(search_key)
            db.session.flush()
    except:
        current_app.logger.info(traceback.format_exc())

        current_app.logger.info("获取项目命名空间-异常！")
    finally:
        current_app.logger.info("获取项目命名空间结束！")


def get_tapd_map_task(task_type):
    search_programs = db.session.query(SysProgram).filter(SysProgram.tapd_work_ids != "").all()
    work_item = {}
    for program in search_programs:
        for work_id in json.loads(program.tapd_work_ids):
            work_item[work_id] = get_tapd_map(work_id, map_type=task_type)
            search_key = db.session.query(TapdKeyValue).filter(and_(TapdKeyValue.workspace_id == work_id,
                                                                    TapdKeyValue.type == task_type,
                                                                    TapdKeyValue.key == "tapd_map")).first()
            if search_key is None:
                search_key = TapdKeyValue()
                search_key.key = "tapd_map"
                search_key.old_value = ""
                search_key.value = json.dumps(work_item[work_id], ensure_ascii=False)
                search_key.type = task_type
                search_key.workspace_id = work_id
            elif work_item[work_id] and (not search_key.value or (search_key.value and
                                                                  json.loads(search_key.value) != work_item[work_id])):
                search_key.old_value = search_key.value
                search_key.value = json.dumps(work_item[work_id], ensure_ascii=False)
            db.session.add(search_key)
            db.session.flush()


def get_date(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", tz=None):
    return (datetime.now(tz) + relativedelta(years=year, months=month, days=day)).strftime(fmt)


def get_story_tester(work_id, story):
    search_key = db.session.query(TapdKeyValue).filter(and_(TapdKeyValue.workspace_id == work_id,
                                                            TapdKeyValue.type == "story_fields_info",
                                                            TapdKeyValue.key == "tapd_map")).first()
    story_fields_info = json.loads(search_key.value)
    tester_key = None
    for item in story_fields_info:
        if "label" in story_fields_info[item].keys() and story_fields_info[item]["label"] == "测试人员":
            tester_key = item
            break
    return story["Story"][tester_key] if tester_key is not None else ""


def get_story_category(work_id, story):
    search_key = db.session.query(TapdKeyValue).filter(and_(TapdKeyValue.workspace_id == work_id,
                                                            TapdKeyValue.type == "story_fields_info",
                                                            TapdKeyValue.key == "tapd_map")).first()
    story_fields_info = json.loads(search_key.value)
    category_id = story["Story"]["category_id"]
    category_name = None
    for item in story_fields_info:
        if item == "category_id" and category_id in story_fields_info["category_id"]["options"].keys():
            category_name = story_fields_info["category_id"]["options"][category_id]
            break
        if item == "category_id" and category_id not in story_fields_info["category_id"]["options"].keys():
            category_name = None
            break
    return category_name
