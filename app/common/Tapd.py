#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/10/22
 @file: Tapd.py
 @site:
 @email:
"""
import json
import os
import time
import traceback
from datetime import datetime
import calendar

import gitlab
import requests
from flask import current_app
from sqlalchemy import and_

from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.JenkinsJobDb import JenkinsJob
from app.models.KeyValueDb import KeyValue
from app.models.SysProgramDb import SysProgram
from app.models.TapdKeyValueDb import TapdKeyValue
from app.tools.tools import send_tv


def get_tapd_api(path):
    """
    获取tapd对应的请求
    :param path: 需要请求的地址
    :return: 返回对应的请求结果
    """
    api_user = "z+8ufHJ="
    api_password = "6102A018-D5F5-D61C-4275-5452B3DA9925"
    get_url = os.path.join("https://api.tapd.cn/", path)
    ret = {
        "data": []
    }
    try:
        r = requests.get(get_url, auth=(api_user, api_password))
        time.sleep(2)
        ret = r.json()
    except:
        send_tv(traceback.format_exc())
    return ret


def get_current_iteration(work_id, end_time):
    ret = ""
    tapd = TapdKeyValue.query.filter(and_(TapdKeyValue.type == "iteration",
                                          TapdKeyValue.key == "tapd_info",
                                          TapdKeyValue.workspace_id == work_id)).first()
    if tapd is not None:
        for item in json.loads(tapd.value):
            start_date = datetime.strptime(item["startdate"], '%Y-%m-%d').date()
            end_date = datetime.strptime(item["enddate"], '%Y-%m-%d').date()
            if start_date <= end_time <= end_date:
                ret = item["id"]
                break
    return ret


def get_current_iteration_all(work_id, end_time):
    ret = []
    tapd = TapdKeyValue.query.filter(and_(TapdKeyValue.type == "iteration",
                                          TapdKeyValue.key == "tapd_info",
                                          TapdKeyValue.workspace_id == work_id)).first()
    if tapd is not None:
        for item in json.loads(tapd.value):
            start_date = datetime.strptime(item["startdate"], '%Y-%m-%d').date()
            end_date = datetime.strptime(item["enddate"], '%Y-%m-%d').date()
            if start_date <= end_time <= end_date:
                ret.append(item["id"])
    return ret


def get_iteration_info(work_id, end_time):
    ret = ""
    tapd = TapdKeyValue.query.filter(and_(TapdKeyValue.type == "iteration",
                                          TapdKeyValue.key == "tapd_info",
                                          TapdKeyValue.workspace_id == work_id)).first()
    if tapd is not None:
        for item in json.loads(tapd.value):
            start_date = datetime.strptime(item["startdate"], '%Y-%m-%d').date()
            end_date = datetime.strptime(item["enddate"], '%Y-%m-%d').date()
            if start_date <= end_time <= end_date:
                ret = item
                break
    return ret


def get_iteration_date(work_id, iteration_id):
    ret = "", ""
    tapd = TapdKeyValue.query.filter(and_(TapdKeyValue.type == "iteration",
                                          TapdKeyValue.key == "tapd_info",
                                          TapdKeyValue.workspace_id == work_id)).first()
    if tapd is not None:
        for item in json.loads(tapd.value):
            if item["id"] == iteration_id:
                start_date = datetime.strptime(item["startdate"], '%Y-%m-%d').date()
                end_date = datetime.strptime(item["enddate"], '%Y-%m-%d').date()
                ret = start_date, end_date
                break
    return ret


def post_tapd_api(path, data):
    api_user = "z+8ufHJ="
    api_password = "6102A018-D5F5-D61C-4275-5452B3DA9925"
    post_url = os.path.join("https://api.tapd.cn/", path)
    try:
        r = requests.post(post_url, auth=(api_user, api_password), json=data)
        ret = r.json()
    except:
        print(traceback.format_exc())
        ret = r.text
    return ret


def get_tapd_map(work_id, map_type):
    if map_type == "iteration":
        url = "iterations?workspace_id={0}".format(work_id)
    elif map_type == "workspace":
        url = "workspaces/projects?company_id={0}".format(work_id)
    elif map_type == "story_fields_info":
        url = "stories/get_fields_info?workspace_id={0}".format(work_id)
    else:
        url = "workflows/status_map?system={0}&workspace_id={1}".format(map_type, work_id)
    tapd_ret = get_tapd_api(url)
    ret = {}
    if map_type == "iteration":
        ret[work_id] = []
        for iteration in tapd_ret["data"]:
            ret[iteration["Iteration"]["id"]] = iteration["Iteration"]["name"]
            ret[work_id].append(iteration)
    elif map_type == "iteration":
        for workspace in tapd_ret["data"]:
            ret[workspace["Workspace"]["id"]] = workspace["Workspace"]["name"]
    elif map_type == "story_fields_info":
        ret = tapd_ret["data"]
    else:
        ret = tapd_ret["data"]
    return ret


def get_tapd_story(work_id, query_end_time=None, query_start_time=None, iteration_id=None):
    if query_start_time is not None or query_end_time is not None:
        if query_start_time is not None:
            url = "stories?workspace_id={0}&created=>{1}".format(work_id, query_start_time)
        elif query_end_time is not None:
            url = "stories?workspace_id={0}&created<={1}".format(work_id, query_end_time)
        elif query_start_time is not None and query_end_time is not None:
            url = "stories?workspace_id={0}&created={1}~{2}".format(work_id, query_start_time, query_end_time)
        else:
            url = "stories?workspace_id={0}".format(work_id)
        if iteration_id is not None:
            url += "&iteration_id={0}".format(iteration_id)
    elif iteration_id is not None:
        url = "stories?workspace_id={0}&iteration_id={1}".format(work_id, iteration_id)
    else:
        url = "stories?workspace_id={0}".format(work_id)
    ret = []
    icount = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        icount += 1
    return ret


# 获取需求变更历史
def get_tapd_story_changes(work_id, story_id):
    url = "story_changes?workspace_id={0}&story_id={1}".format(work_id, story_id)
    ret = []
    i = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, i)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        i += 1
    return ret


def get_special_status_story_completed_time(work_id, story_id):
    story_changes = get_tapd_story_changes(work_id, story_id)
    for change in story_changes:
        changes = change["WorkitemChange"]["changes"]
        if changes != "[]":
            value_after = json.loads(changes)[0]["value_after"]
        #  status_1：线上观察，财务系统特有状态
        if change["WorkitemChange"]["change_summary"] in ("testing", "status_4") and value_after == "status_1":
            completed_time = change["WorkitemChange"]["created"]
    return completed_time


def get_tapd_test_plan(work_id, query_end_time=None, query_start_time=None, iteration_id=None):
    if query_start_time is not None or query_end_time is not None:
        if query_start_time is not None:
            url = "test_plans?workspace_id={0}&created=>{1}".format(work_id, query_start_time)
        elif query_end_time is not None:
            url = "test_plans?workspace_id={0}&created<={1}".format(work_id, query_end_time)
        elif query_start_time is not None and query_end_time is not None:
            url = "test_plans?workspace_id={0}&created={1}~{2}".format(work_id, query_start_time, query_end_time)
        else:
            url = "test_plans?workspace_id={0}".format(work_id)
        if iteration_id is not None:
            url += "&iteration_id={0}".format(iteration_id)
    elif iteration_id is not None:
        url = "test_plans?workspace_id={0}&iteration_id={1}".format(work_id, iteration_id)
    else:
        url = "test_plans?workspace_id={0}".format(work_id)
    ret = []
    icount = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        icount += 1
    return ret


def get_tapd_story_for_status(work_id, status=["for_test"]):
    url = "stories?workspace_id={0}".format(work_id)
    ret = []
    icount = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        print(send_url)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        icount += 1
    real_ret = []
    for story in ret:
        if story["Story"]["status"] in status:
            real_ret.append(story)
    return real_ret


def get_tapd_case(work_id, query_end_time=None, query_start_time=None):
    if query_start_time is not None:
        url = "tcases?workspace_id={0}&created=>{1}".format(work_id, query_start_time)
    elif query_end_time is not None:
        url = "tcases?workspace_id={0}&created<={1}".format(work_id, query_end_time)
    elif query_start_time is not None and query_end_time is not None:
        url = "tcases?workspace_id={0}&created={1}~{2}".format(work_id, query_start_time, query_end_time)
    else:
        url = "tcases?workspace_id={0}".format(work_id)

    ret = []
    icount = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        icount += 1
    return ret


def get_tapd_bug(work_id, query_end_time=None, query_start_time=None, iteration_id=None):
    if query_start_time is not None or query_end_time is not None:
        if query_start_time is not None:
            url = "bugs?workspace_id={0}&created=>{1}".format(work_id, query_start_time)
        elif query_end_time is not None:
            url = "bugs?workspace_id={0}&created<={1}".format(work_id, query_end_time)
        elif query_start_time is not None and query_end_time is not None:
            url = "bugs?workspace_id={0}&created={1}~{2}".format(work_id, query_start_time, query_end_time)
        else:
            url = "bugs?workspace_id={0}".format(work_id)
        if iteration_id is not None:
            url += "&iteration_id={0}".format(iteration_id)
    elif iteration_id is not None:
        url = "bugs?workspace_id={0}&iteration_id={1}".format(work_id, iteration_id)
    else:
        url = "bugs?workspace_id={0}".format(work_id)
    ret = []
    icount = 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        send_ret = get_tapd_api(send_url)["data"]
        if send_ret:
            print("{0}, {1}".format("有数据", send_url))
        else:
            print("{0}, {1}".format(send_ret, send_url))
            break
        ret += send_ret
        icount += 1
    return ret


def get_relations(work_id, target_id, relation_type="bug", get_type="story"):
    url = "relations?workspace_id={0}&target_type={1}&target_id={2}".format(work_id, get_type, target_id)
    get_tapd_api(url)
    url = "relations?workspace_id={0}&source_type={1}&source_id={2}".format(work_id, relation_type, target_id)
    get_ret, send_rets, icount = [], [], 1
    while True:
        send_url = "{0}&limit=200&page={1}".format(url, icount)
        send_ret = get_tapd_api(send_url)["data"]
        if not send_ret:
            break
        send_rets += send_ret
        icount += 1
    for ret in send_rets:
        if ret["Relation"]["target_type"] == get_type:
            get_ret.append(ret["Relation"]["target_id"])
    return get_ret


def get_relations_by_story(work_id, story_id):
    url = "stories/get_story_tcase?workspace_id={0}&story_id={1}".format(work_id, story_id)
    ret = get_tapd_api(url)["data"]
    print("{0}{2}, {1}".format("有数据", url, len(ret)))
    return ret


def get_git_commit(system, branch, start_time, end_time):

    get_ret = {
        "code": 1,
        "msg": "失败",
        "data": []
    }
    data = {
        "system": system,
        "branch": branch,
        "startDate": start_time,
        "endDate": end_time
        }
    try:
        headers = {"Content-Type": "application/json"}
        find_task = AssumptBuildTask.query.filter(and_(AssumptBuildTask.program_id == system,
                                                       AssumptBuildTask.build_branch == branch)).first()
        print(find_task.build_jenkins_jobs)
        if find_task:
            jenkins_url = json.loads(find_task.build_jenkins_jobs)[0]["url"]
            if jenkins_url:
                print(current_app.config["JENKINS_DICT"][jenkins_url]["JACOCO_HOST"] +
                                    current_app.config["GIT_MONTH_INFO"])
                req = requests.post(current_app.config["JENKINS_DICT"][jenkins_url]["JACOCO_HOST"] +
                                    current_app.config["GIT_MONTH_INFO"], json=data, headers=headers)
                if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                    get_ret["code"] = 0
                    get_ret["msg"] = "获取成功"
                    get_ret["data"] = req.json()["data"]
            else:
                get_ret["msg"] = "the jenkins's url is empty"
        else:
            get_ret["msg"] = "not found the task's info"
    except:
        current_app.logger.error(traceback.format_exc())
    current_app.logger.info("get_git_commit, system is :{0}, branch is {1}, data is {2}".format(system,
                                                                                                branch,
                                                                                                get_ret["data"]))
    return get_ret


def get_story_case_info(work_id, story_id):
    return get_relations(work_id, story_id, relation_type="story", get_type="tcase")


def get_build_branch(program_name, msg):
    """
    :param msg: 匹配的提交信息，默认是需求ID
    :param program_name: 获取分支的项目名称
    :return: 返回提交的项目名，分支名
    """
    gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
    gl.auth()
    ret_data = []
    ret = {
            "code": 1,
            "data": ret_data,
            "msg": "success"
    }
    try:
        git_program_ids = SysProgram.query.filter(
            SysProgram.sys_program_desc == program_name).first().git_program_ids
        if git_program_ids is not None and len(git_program_ids) > 0:
            projects = json.loads(git_program_ids).values()
        else:
            projects = []
        msg = msg.split(",") if "," in msg else [msg]
        for project_id in projects:
            try:
                project = gl.projects.get(project_id)
                branches = project.branches.list(all=True)
                is_found = False
                for branch in branches:
                    create_at = datetime.strptime(branch.attributes["commit"]["created_at"],
                                                  "%Y-%m-%dT%H:%M:%S.000+00:00")
                    if (datetime.now() - create_at).days < 30:
                        branch_commits = project.commits.list(ref_name=branch.attributes["name"], per_page=100)
                        for item_commit in branch_commits:
                            if list(filter(lambda x: x in item_commit.attributes["message"], msg)):
                                if branch.attributes["name"] != "master" and \
                                        not item_commit.attributes["message"].startswith("Merge branch") and \
                                        project.id not in list(map(lambda x: x["program"], ret_data)):
                                    ret_data.append({"branch": branch.attributes["name"],
                                                     "program": project.id})
                                    is_found = True
                                    break
                            if is_found:
                                break
                ret["code"] = 0
            except Exception as e:
                current_app.logger.error(e)
                current_app.logger.error(traceback.format_exc())
                send_tv(traceback.format_exc())

        if not ret_data:
            ret_data.append({
                "branch": "master",
                "program": 0
            })
        current_app.logger.info(ret_data)
    except Exception as e:
        current_app.logger.error(e)
        current_app.logger.error(traceback.format_exc())
        send_tv(traceback.format_exc())
        pass
    current_app.logger.info("get branch {0} {1} {2}".format(program_name, msg, json.dumps(ret_data)))
    return ret


def create_iteration(work_id, name, startdate, enddate):
    url = "iterations"
    body = {"name": name,
            "workspace_id": work_id,
            "startdate": startdate,
            "enddate": enddate,
            "creator": "刘田宝"
            }
    print(post_tapd_api(url, body))


if __name__ == "__main__":
    from pprint import pprint
    storys = get_tapd_story(21691821, '2023-01-01')
    pprint(storys[0])
    # for i in range(4, 13):
    #     work_id = "23670891"
    #     name = "清结算2023" + datetime(2023, i, 1).strftime("%m")
    #     start = datetime(2023, i, 1).strftime("%Y-%m-%d")
    #     end = datetime(2023, i, calendar.monthrange(2023, i)[1]).strftime("%Y-%m-%d")
    #     print(name, start, end)
    #     create_iteration(work_id, name, start, end)
    #     time.sleep(1)
