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
from datetime import datetime
from copy import deepcopy

from dateutil.relativedelta import relativedelta
from flask import jsonify, current_app
from sqlalchemy import and_, func

from app import db
from app.api.statis_report import api_statistics_report
import traceback
import json

from app.common.Tapd import get_iteration_info
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.AssumptBuildTaskRunDb import AssumptBuildTaskRun
from app.models.GitMergeInfoDb import GitMergeInfo
from app.models.SonarInfoDb import SonarInfo
from app.models.SysProgramDb import SysProgram
from app.models.TapdBugDetailDb import TapdBugDetail
from app.models.TapdStoryDetailDb import TapdStoryDetail
from app.models.GitTagInfoDb import GitTagInfo
from app.models.TapdTestPlanDetailDb import TapdTestPlanDetail
from app.models.CoverageInfoDb import CoverageInfo

from app.tools.tools import send_tv

RATE_DICT = {
    1.0: "A",
    2.0: "B",
    3.0: "C",
    4.0: "D",
    5.0: "E"
}

SONAR_SORT = {
    "国内放款项目": 1,
    "海外放款项目": 2,
    "国内合同项目": 3,
    "国内费率项目": 4,
    "国内还款项目": 5,
    "海外还款项目": 6,
    "国内支付项目": 7,
    "海外支付项目": 8,
    "国内清结算项目": 9,
    "海外清结算项目": 10,
}

STORY_STATUS = {
    "new": "新建",
    "closed": "已关闭",
    "in_progress": "",
    "rejected": "已拒绝",
    "resolved": "已解决",
    "verified": "已验证",
    "reopened": "重新打开",
    "suspended": "挂起"
}

MAX_SONAR_NUM = 11


@api_statistics_report.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Statistics report!'


@api_statistics_report.route('/get_total_data/<int:day>', methods=['GET', 'POST'])
def get_total_data(day=7):
    start_date = get_date(day=-day, fmt="%Y-%m-%d  00:00:00")
    end_date = get_date(day=0, fmt="%Y-%m-%d  23:59:59")
    tags = len(GitTagInfo.query.filter(GitTagInfo.tag_create >= start_date,
                                       GitTagInfo.tag_create <= end_date).all())
    bugs = len(TapdBugDetail.query.filter(TapdBugDetail.bug_create >= start_date,
                                          TapdBugDetail.bug_create <= end_date).all())
    onlines = len(TapdBugDetail.query.filter(
        TapdBugDetail.bug_create >= start_date,
        TapdBugDetail.bug_create <= end_date,
        TapdBugDetail.find_version.like("%online%")).all())
    ret = {
        "code": 0,
        "msg": "get data success",
        "data": {"tags": tags,
                 "bugs": bugs,
                 "onlines": onlines}
    }
    return jsonify(ret)


@api_statistics_report.route('/story_bug_build/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def get_story_bug_build(start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get story bug build error",
        "data": []
    }
    try:
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        days = (end_date - start_date).days + 1
        search_programs = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
        total_data = []
        for program in search_programs:
            data = dict()
            data["program_id"] = program.sys_program_id
            data["program_name"] = program.sys_program_name
            data["organization"] = program.sys_program_group_id
            if program.tapd_work_ids is not None and len(program.tapd_work_ids) > 0:
                tapd_id_list = json.loads(program.tapd_work_ids)
                data["bug_created"] = len(TapdBugDetail.query.filter(TapdBugDetail.bug_workspace_id.in_(tapd_id_list),
                                                                     TapdBugDetail.bug_create >= start_date,
                                                                     TapdBugDetail.bug_create <= end_date).all())
                data["story_publish"] = len(
                    TapdStoryDetail.query.filter(TapdStoryDetail.story_workspace_id.in_(tapd_id_list),
                                                 TapdStoryDetail.story_completed >= start_date,
                                                 TapdStoryDetail.story_completed <= end_date,
                                                 TapdStoryDetail.story_iteration_id != "0").all())
                data["build_average"] = len(
                    AssumptBuildTaskRun.query.filter(AssumptBuildTaskRun.build_program_id == program.sys_program_id,
                                                     AssumptBuildTaskRun.build_time >= start_date,
                                                     AssumptBuildTaskRun.build_time <= end_date).all()) // days
            else:
                data["bug_created"] = data["story_publish"] = data["build_average"] = 0
            total_data.append(data)
        ret["data"] = total_data
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get story bug build success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/tag_online_bug/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def get_tag_online(start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get tag_online error",
        "data": []
    }
    try:
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        search_programs = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
        total_data = []
        for program in search_programs:
            data = dict()
            data["program_id"] = program.sys_program_id
            data["program_name"] = program.sys_program_name
            data["organization"] = program.sys_program_group_id
            data["tag_created"] = 0
            if program.git_program_ids is not None and len(program.git_program_ids) > 0:
                for git_name, git_id in json.loads(program.git_program_ids).items():
                    if git_name.startswith("OA"):
                        data["tag_created"] += len(GitMergeInfo.query.filter(GitMergeInfo.gitlab_id == git_id,
                                                                             GitMergeInfo.merge_create > start_date,
                                                                             GitMergeInfo.merge_create < end_date).group_by(GitMergeInfo.source_branch).all())
                    else:
                        data["tag_created"] += len(GitTagInfo.query.filter(GitTagInfo.tag_gitlab_id == git_id,
                                                                           GitTagInfo.tag_create >= start_date,
                                                                           GitTagInfo.tag_create <= end_date).all())
            else:
                data["tag_created"] = 0

            if program.tapd_work_ids is not None and len(program.tapd_work_ids) > 0:
                tapd_id_list = json.loads(program.tapd_work_ids)
                # 13：贷后系统,24：财务系统,25：线上问题跟踪
                if program.sys_program_group_id != 10:
                    data["online_bug_created"] = len(
                        TapdBugDetail.query.filter(TapdBugDetail.bug_workspace_id.in_(tapd_id_list),
                                                   TapdBugDetail.bug_create >= start_date,
                                                   TapdBugDetail.bug_create <= end_date,
                                                   TapdBugDetail.find_version.like("%online%")).all())
                elif program.sys_program_group_id == 10 and program.sys_program_id == 13:
                    data["online_bug_created"] = len(
                        TapdBugDetail.query.filter(TapdBugDetail.bug_workspace_id == 20270071,
                                                   TapdBugDetail.bug_create >= start_date,
                                                   TapdBugDetail.bug_create <= end_date,
                                                   TapdBugDetail.find_version == "贷后系统").all())
                elif program.sys_program_group_id == 10 and program.sys_program_id == 24:
                    data["online_bug_created"] = len(
                        TapdBugDetail.query.filter(TapdBugDetail.bug_workspace_id == 20270071,
                                                   TapdBugDetail.bug_create >= start_date,
                                                   TapdBugDetail.bug_create <= end_date,
                                                   TapdBugDetail.find_version.in_(["财务系统", "OA系统"])).all())
                else:
                    data["online_bug_created"] = 0
            else:
                data["online_bug_created"] = 0
            total_data.append(data)
        ret["data"] = total_data
        ret["msg"] = "get tag_online success"
        ret["code"] = 0
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    return jsonify(ret)


@api_statistics_report.route('/coverage/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def get_coverage(start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get coverage error",
        "data": []
    }
    try:
        calc_time = '{0}至{1}'.format(start_date, end_date)
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        program_list = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
        for program in program_list:
            data = dict()
            data["calc_time"] = calc_time
            data["program_id"] = program.sys_program_id
            data["program_name"] = program.sys_program_name
            data["organization"] = program.sys_program_group_id
            data["total_add_lines"] = 0
            data["total_del_lines"] = 0
            data["total_commit_count"] = 0
            data["total_change_files"] = 0
            data["total_coverage"] = 0
            data["branch_count"] = 0
            data["miss_count"] = 0
            data["average_coverage"] = 0
            data["change_code"] = 0
            if program.git_program_ids is not None and len(program.git_program_ids) > 0:
                git_id_list = json.loads(program.git_program_ids).values()
                branchs = db.session.query(func.sum(GitMergeInfo.git_add_lines).label("add_line"),
                                           func.sum(GitMergeInfo.git_remove_lines).label("remove_line"),
                                           func.sum(GitMergeInfo.git_changed_file).label("change_file"),
                                           func.sum(GitMergeInfo.git_commit_count).label("commit_count"),
                                           GitMergeInfo.source_branch,
                                           GitMergeInfo.gitlab_id,
                                           GitMergeInfo.gitlab_name).filter(GitMergeInfo.gitlab_id.in_(git_id_list),
                                                                            GitMergeInfo.merge_create > start_date,
                                                                            GitMergeInfo.merge_create < end_date). \
                    group_by(GitMergeInfo.source_branch, GitMergeInfo.gitlab_id).all()
            else:
                branchs = []
            tapd_id_list = json.loads(program.tapd_work_ids)
            for branch in branchs:
                # 如果在其他项目中发现有需求关联，则是其他项目的，跳过统计
                other_story_info = AssumptBuildTask.query.filter(AssumptBuildTask.build_branch == branch.source_branch,
                                                                 AssumptBuildTask.gitlab_program_id == branch.gitlab_id,
                                                                 AssumptBuildTask.work_id.notin_(tapd_id_list)).first()

                story_info = AssumptBuildTask.query.filter(AssumptBuildTask.build_branch == branch.source_branch,
                                                           AssumptBuildTask.gitlab_program_id == branch.gitlab_id,
                                                           AssumptBuildTask.work_id.in_(tapd_id_list)).first()

                if story_info is None and other_story_info is not None:
                    continue
                data["total_add_lines"] = data["total_add_lines"] + int(branch.add_line)
                data["total_del_lines"] = data["total_del_lines"] + int(branch.remove_line)
                data["total_commit_count"] = data["total_commit_count"] + int(branch.commit_count)
                data["total_change_files"] = data["total_change_files"] + int(branch.change_file)
                data["change_code"] = data["change_code"] + int(branch.add_line) + int(branch.remove_line)
                last_coverage, max_coverage, from_new, coverage_url = \
                    get_coverage_with_branch(branch.gitlab_id, branch.source_branch)

                if last_coverage is None or last_coverage == 0:
                    data["miss_count"] = data["miss_count"] + 1
                else:
                    data["branch_count"] = data["branch_count"] + 1
                    data["total_coverage"] = data["total_coverage"] + last_coverage
            data["average_coverage"] = '{0}%'.format(round(data["total_coverage"] / data["branch_count"], 2)) \
                if data["branch_count"] else '0%'
            ret["data"].append(data)
        ret["msg"] = "get coverage success"
        ret["code"] = 0
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get coverage success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/sonar/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def get_sonar(start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get sonar error",
        "data": []
    }
    try:
        # start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        program_list = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
        for program in program_list:
            if program.sys_sonar_key is not None and len(program.sys_sonar_key) > 0:
                for program_name, program_key in json.loads(program.sys_sonar_key).items():
                    data = dict()
                    sonar_info = SonarInfo.query.filter(SonarInfo.sonar_branch_time <= end_date,
                                                        SonarInfo.sonar_program_key == program_key,
                                                        SonarInfo.sonar_branch == 'master').order_by(
                        SonarInfo.sonar_branch_time.desc()).first()

                    if sonar_info is None:
                        continue
                    sonar_info = sonar_info.serialize()
                    for key, value in sonar_info.items():
                        data[key] = value
                    data["program_id"] = program.sys_program_id
                    data["program_name"] = program.sys_program_name
                    data["organization"] = program.sys_program_group_id
                    ret["data"].append(data)

        for sonar_item in ret["data"]:
            sonar_item["sonar_security_rating"] = RATE_DICT[sonar_item["sonar_security_rating"]]
            sonar_item["sonar_reliability_rating"] = RATE_DICT[sonar_item["sonar_reliability_rating"]]
            sonar_item["sonar_sqale_rating"] = RATE_DICT[sonar_item["sonar_sqale_rating"]]
            sonar_item["sonar_num"] = SONAR_SORT[sonar_item["sonar_program_name"]] if \
                sonar_item["sonar_program_name"] in SONAR_SORT else MAX_SONAR_NUM
        ret["data"] = \
            sorted(ret["data"], key=lambda x: x["sonar_num"], reverse=False)
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get sonar success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/coverage/program/<string:program_name>/<string:start_date>/<string:end_date>',
                             methods=['GET', 'POST'])
def get_coverage_program(program_name, start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get coverage error",
        "average_coverage": 0,
        "branch_count": 0,
        "miss_count": 0,
        "change_code": 0
    }
    try:
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        program = SysProgram.query.filter(SysProgram.sys_program_name == program_name).first()
        if program is None:
            raise ValueError("not found the sys program's id")
        ret["program_id"] = program.sys_program_id
        ret["program_name"] = program.sys_program_name
        ret["change_code"] = 0
        ret["total_coverage"] = 0
        ret["branch_count"] = 0
        ret["miss_count"] = 0
        git_id_list = json.loads(program.git_program_ids).values()
        tapd_id_list = json.loads(program.tapd_work_ids)
        branchs = db.session.query(func.sum(GitMergeInfo.git_add_lines).label("add_line"),
                                   func.sum(GitMergeInfo.git_remove_lines).label("remove_line"),
                                   GitMergeInfo.source_branch,
                                   GitMergeInfo.merge_create_date,
                                   GitMergeInfo.gitlab_id,
                                   GitMergeInfo.gitlab_name).filter(GitMergeInfo.gitlab_id.in_(git_id_list),
                                                                    GitMergeInfo.merge_create > start_date,
                                                                    GitMergeInfo.merge_create < end_date).group_by(
            GitMergeInfo.source_branch, GitMergeInfo.gitlab_id).all()
        data_coverage = list()
        data_no_coverage = list()
        data_temp = dict()
        data_temp["coverage_branch"] = ""
        data_temp["coverage_logic"] = ""
        data_temp["story_url"] = ""
        data_temp["story_name"] = ""
        data_temp["git_name"] = ""
        data_temp["merge_time"] = ""
        data_temp["static_time"] = ""
        data_temp["publish_time"] = ""
        data_temp["publish_week"] = "无覆盖率分支"

        for branch in branchs:
            # 如果在其他项目中发现有需求关联，则是其他项目的，跳过统计
            other_story_info = AssumptBuildTask.query.filter(AssumptBuildTask.build_branch == branch.source_branch,
                                                             AssumptBuildTask.gitlab_program_id == branch.gitlab_id,
                                                             AssumptBuildTask.work_id.notin_(tapd_id_list)).first()

            story_info = AssumptBuildTask.query.filter(AssumptBuildTask.build_branch == branch.source_branch,
                                                       AssumptBuildTask.gitlab_program_id == branch.gitlab_id,
                                                       AssumptBuildTask.work_id.in_(tapd_id_list)).first()

            if story_info is None and other_story_info is not None:
                continue

            if story_info is None:
                story_info = AssumptBuildTask.query.filter(AssumptBuildTask.program_id == program.sys_program_id,
                                                           AssumptBuildTask.build_branch == branch.source_branch,
                                                           AssumptBuildTask.gitlab_program_id.in_(git_id_list),
                                                           AssumptBuildTask.work_id.in_(tapd_id_list)).first()

            ret["change_code"] = ret["change_code"] + int(branch.add_line + branch.remove_line)
            data_temp["change_code"] = int(branch.add_line + branch.remove_line)

            last_coverage, max_coverage, from_new, coverage_url = \
                get_coverage_with_branch(branch.gitlab_id, branch.source_branch)
            data_temp["coverage_url"] = coverage_url
            data_temp["coverage_branch"] = branch.source_branch
            data_temp["coverage_logic"] = last_coverage
            data_temp["coverage_logic_max"] = max_coverage
            data_temp["from_new"] = from_new
            data_temp["story_url"] = story_info.story_url if story_info is not None else ""
            data_temp["story_name"] = story_info.story_name if story_info is not None else ""
            data_temp["git_name"] = branch.gitlab_name
            data_temp["merge_time"] = branch.merge_create_date.strftime("%Y-%m-%d")
            data_temp["static_time"] = story_info.mail_receive_time.strftime("%Y-%m-%d") \
                if story_info is not None else ""
            data_temp["publish_time"] = story_info.publish_time.strftime("%Y-%m-%d") \
                if (story_info is not None and story_info.publish_time is not None) else ""
            data_temp["publish_week"] = get_week_info(story_info.publish_time) \
                if (story_info is not None and story_info.publish_time is not None) else ""

            if last_coverage is None or last_coverage == 0:
                ret["miss_count"] = ret["miss_count"] + 1
                data_no_coverage.append(deepcopy(data_temp))
            else:
                ret["branch_count"] = ret["branch_count"] + 1
                ret["total_coverage"] = ret["total_coverage"] + last_coverage
                data_coverage.append(deepcopy(data_temp))
        ret["average_coverage"] = 0 \
            if int(ret["total_coverage"]) == 0 else round(ret["total_coverage"] / ret["branch_count"], 2)
        ret["data"] = sorted(data_coverage, key=lambda x: (x["git_name"], x["publish_time"]), reverse=True) + \
                      sorted(data_no_coverage, key=lambda x: (x["publish_time"], x["git_name"], x["story_name"]),
                             reverse=True)
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get coverage success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/sonar/program/<string:program_name>/<string:start_date>/<string:end_date>',
                             methods=['GET', 'POST'])
def get_sonar_program(program_name, start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get sonar error",
        "data": []
    }
    try:
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        program = SysProgram.query.filter(SysProgram.sys_program_name == program_name).first()
        git_id_list = json.loads(program.git_program_ids).values()
        ret["program_id"] = program.sys_program_id
        ret["program_name"] = program.sys_program_name

        # 已发布需求，需要展示
        branchs = GitMergeInfo.query.filter(GitMergeInfo.gitlab_id.in_(git_id_list),
                                            GitMergeInfo.merge_create > start_date,
                                            GitMergeInfo.merge_create < end_date).group_by(
            GitMergeInfo.source_branch).all()
        branch_name_list = [branch.source_branch for branch in branchs]

        # 测试中的需求需求，也需要展示出来
        branchs = AssumptBuildTask.query.filter(AssumptBuildTask.gitlab_program_id.in_(git_id_list),
                                                AssumptBuildTask.publish_time == None).all()
        branch_name_list += [branch.build_branch for branch in branchs]

        total_data = list()
        for branch_name in branch_name_list:
            data = dict()
            if program.sys_sonar_key is not None and len(program.sys_sonar_key) > 0:
                sonar_id_list = json.loads(program.sys_sonar_key).values()
                sonar_info = SonarInfo.query.filter(SonarInfo.sonar_program_key.in_(sonar_id_list),
                                                    SonarInfo.sonar_branch == branch_name).order_by(
                    SonarInfo.sonar_branch_time.desc()).first()
                if sonar_info is not None:
                    sonar_info = sonar_info.serialize()
                    for key, value in sonar_info.items():
                        data[key] = value
                    total_data.append(data)

        for sonar_item in total_data:
            sonar_item["sonar_security_rating"] = RATE_DICT[sonar_item["sonar_security_rating"]]
            sonar_item["sonar_reliability_rating"] = RATE_DICT[sonar_item["sonar_reliability_rating"]]
            sonar_item["sonar_sqale_rating"] = RATE_DICT[sonar_item["sonar_sqale_rating"]]
            sonar_item["sonar_num"] = SONAR_SORT[sonar_item["sonar_program_name"]] if \
                sonar_item["sonar_program_name"] in SONAR_SORT else MAX_SONAR_NUM

        ret["data"] = \
            sorted(total_data, key=lambda x: (x["sonar_num"], x["sonar_branch_time"]), reverse=False)
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get sonar success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/commit/program/<string:program_name>/<string:start_date>/<string:end_date>',
                             methods=['GET'])
def get_commit_program(program_name, start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get git_commit error",
        "rows": []
    }
    try:
        start_date = datetime.strptime(start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        program = SysProgram.query.filter(SysProgram.sys_program_name == program_name).first()
        git_id_list = json.loads(program.git_program_ids).values()
        ret["program_id"] = program.sys_program_id
        ret["program_name"] = program.sys_program_name

        branchs = GitMergeInfo.query.filter(GitMergeInfo.gitlab_id.in_(git_id_list),
                                            GitMergeInfo.merge_create > start_date,
                                            GitMergeInfo.merge_create < end_date).group_by(
            GitMergeInfo.source_branch, GitMergeInfo.gitlab_id).all()
        total_data = list()
        for branch in branchs:
            data = dict()
            for key, value in branch.serialize().items():
                data[key] = value
            total_data.append(data)
        ret["data"] = total_data
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get git_commit data success"
        ret["code"] = 0
    return jsonify(ret)


@api_statistics_report.route('/iteration/program/<string:program_name>/<string:start_date>/<string:end_date>',
                             methods=['GET'])
def get_iteration_program(program_name, start_date, end_date):
    ret = {
        "code": 1,
        "msg": "get iteration program error",
        "rows": []
    }
    try:
        end_date = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        program = SysProgram.query.filter(SysProgram.sys_program_name == program_name).first()
        tapd_id_list = json.loads(program.tapd_work_ids)

        ret["program_id"] = program.sys_program_id
        ret["program_name"] = program.sys_program_name

        iteration_id_list = []
        for tapd_id in tapd_id_list:
            iteration_info = get_iteration_info(tapd_id, end_date.date())
            iteration_id_list.append(iteration_info["id"])
        # story_close_statu_list = ["resolved", "status_2", "status_1"]
        story_info = dict()
        story_info["story_total"] = len(
            TapdStoryDetail.query.filter(TapdStoryDetail.story_iteration_id.in_(iteration_id_list)).all())
        story_info["story_close"] = len(
            TapdStoryDetail.query.filter(TapdStoryDetail.story_iteration_id.in_(iteration_id_list),
                                         TapdStoryDetail.story_status == "resolved").all())
        story_info["close_url"] = "https://www.tapd.cn/{0}/prong/stories/stories_list?" \
                                  "data[Filter][iteration_id][]={1}&qksearch=true&data[Filter][status][]={2}&" \
                                  "qksearch=true".format(tapd_id_list[0], iteration_id_list[0], "resolved")
        story_info["total_url"] = "https://www.tapd.cn/{0}/prong/stories/stories_list?data[Filter][iteration_id][]" \
                                  "={1}&qksearch=true".format(tapd_id_list[0], iteration_id_list[0])

        bug_info = dict()
        bug_info["bug_total"] = len(
            TapdBugDetail.query.filter(TapdBugDetail.bug_iteration_id.in_(iteration_id_list)).all())
        bug_info["bug_close"] = len(TapdBugDetail.query.filter(TapdBugDetail.bug_iteration_id.in_(iteration_id_list),
                                                               TapdBugDetail.bug_status == "closed").all())
        bug_info["close_url"] = "https://www.tapd.cn/{0}/bugtrace/bugreports/my_view?filter=" \
                                "true&data[Filter][iteration_id][]={1}&data[Filter][status][]=" \
                                "closed&qksearch=true&qksearch=true".format(tapd_id_list[0], iteration_id_list[0])
        bug_info["total_url"] = "https://www.tapd.cn/{0}/bugtrace/bugreports/my_view?filter=true&data[Filter]" \
                                "[iteration_id][]={1}&qksearch=true&qksearch=true".format(tapd_id_list[0],
                                                                                          iteration_id_list[0])

        online_bug_info = dict()
        if program.sys_program_id not in (13, 24):
            online_bug_info["bug_total"] = len(
                TapdBugDetail.query.filter(TapdBugDetail.bug_iteration_id.in_(iteration_id_list),
                                           TapdBugDetail.find_version == 'online_bug').all())
            online_bug_info["bug_close"] = len(
                TapdBugDetail.query.filter(TapdBugDetail.bug_iteration_id.in_(iteration_id_list),
                                           TapdBugDetail.bug_status == "closed",
                                           TapdBugDetail.find_version == 'online_bug').all())
            online_bug_info["close_url"] = "https://www.tapd.cn/{0}/bugtrace/bugreports/my_view?filter" \
                                           "=true&data[Filter][iteration_id][]={1}&data[Filter][status][]" \
                                           "=closed&data[Filter][version_report][]=online%20bug&qksearch" \
                                           "=true&qksearch=true".format(tapd_id_list[0], iteration_id_list[0])

            online_bug_info["total_url"] = "https://www.tapd.cn/{0}/bugtrace/bugreports/my_view?" \
                                           "filter=true&data[Filter][iteration_id][]={1}&" \
                                           "data[Filter][version_report][]=online%20bug&" \
                                           "qksearch=true&qksearch=true".format(tapd_id_list[0], iteration_id_list[0])
        else:
            online_bug_info["bug_total"] = len(
                TapdBugDetail.query.filter(TapdBugDetail.bug_create_date >= start_date,
                                           TapdBugDetail.bug_create_date <= end_date.date(),
                                           TapdBugDetail.bug_workspace_id.in_(tapd_id_list)).all())
            online_bug_info["bug_close"] = len(
                TapdBugDetail.query.filter(TapdBugDetail.bug_create_date >= start_date,
                                           TapdBugDetail.bug_create_date <= end_date.date(),
                                           TapdBugDetail.bug_workspace_id.in_(tapd_id_list),
                                           TapdBugDetail.bug_status == "closed").all())
            online_bug_info["close_url"] = "https://www.tapd.cn/20270071/bugtrace/bugreports/my_view?" \
                                           "filter=true&data[Filter][status][]=closed" \
                                           "&data[Filter][created][begin]={0}%2000%3A00" \
                                           "&data[Filter][created][end]={1}%2023%3A59" \
                                           "&qksearch=true" \
                                           "&data[Filter][custom_field_one][]=%E8%B4%B7%E5%90%8E%E7%B3%BB%E7%BB%9F" \
                                           "&qksearch=true".format(start_date, end_date.date())

            online_bug_info["total_url"] = "https://www.tapd.cn/20270071/bugtrace/bugreports/my_view?" \
                                           "data[Filter][created][begin]={0}%2000%3A00" \
                                           "&data[Filter][created][end]={1}%2023%3A59" \
                                           "&qksearch=true" \
                                           "&data[Filter][custom_field_one][]=%E8%B4%B7%E5%90%8E%E7%B3%BB%E7%BB%9F" \
                                           "&qksearch=true".format(start_date, end_date.date())
        test_plan_info = dict()
        test_plan_info["test_plan_total"] = len(
            TapdTestPlanDetail.query.filter(TapdTestPlanDetail.test_plan_iteration_id.in_(iteration_id_list)).all())
        test_plan_info["test_plan_close"] = len(
            TapdTestPlanDetail.query.filter(TapdTestPlanDetail.test_plan_iteration_id.in_(iteration_id_list),
                                            TapdTestPlanDetail.test_plan_status == "close").all())
        test_plan_info["close_url"] = "https://www.tapd.cn/{0}/sparrow/test_plan/plan_list?data[Filter]" \
                                      "[status][]=close&qksearch=true&qksearch=true".format(tapd_id_list[0])
        test_plan_info["total_url"] = "https://www.tapd.cn/{0}/sparrow/test_plan/plan_list".format(tapd_id_list[0])

        ret["data"] = {
            "story": story_info,
            "bug": bug_info,
            "online_bug": online_bug_info,
            "test_plan": test_plan_info
        }
    except Exception as e:
        current_app.logger.error(e)
        send_tv(traceback.format_exc())
    else:
        ret["msg"] = "get program data iteration success"
        ret["code"] = 0
    return jsonify(ret)


def get_week_info(publish_time):
    if not isinstance(publish_time, datetime):
        return publish_time
    month = publish_time.month
    year = publish_time.year
    week_begin = datetime.strptime("{0}{1}01".format(year, month), "%Y%m%d").strftime("%W")
    week_now = publish_time.strftime("%W")
    ret = "{0}月第{1}周".format(month, int(week_now) - int(week_begin) + 1)
    return ret


def get_coverage_with_branch(git_id, branch_name):
    env_list = db.session.query(CoverageInfo.service_name, CoverageInfo.env). \
        filter(CoverageInfo.gitlab_program_id == git_id, CoverageInfo.compare_branch == branch_name). \
        group_by(CoverageInfo.service_name, CoverageInfo.env).all()
    last_coverage = max_coverage = 0
    coverage_url = ""
    for env in env_list:
        coverage = CoverageInfo.query.filter(CoverageInfo.gitlab_program_id == git_id,
                                             CoverageInfo.compare_branch == branch_name,
                                             CoverageInfo.service_name == env.service_name,
                                             CoverageInfo.env == env.env).order_by(
            CoverageInfo.version.desc()).first()
        if coverage is None:
            last_coverage = 0
        else:
            if int(coverage.line_coverage) > 0 and int(coverage.line_coverage) > int(last_coverage):
                last_coverage = coverage.line_coverage
                coverage_url = coverage.coverage_url

        # coverage = db.session.query(func.max(CoverageInfo.line_coverage).label("line_coverage")).filter(
        #     CoverageInfo.gitlab_program_id == git_id,
        #     CoverageInfo.compare_branch == branch_name,
        #     CoverageInfo.service_name == env.service_name,
        #     CoverageInfo.env == env.env
        # ).first()
        # if coverage is None:
        #     max_coverage = 0
        # else:
        #     if int(coverage.line_coverage) > 0 and int(coverage.line_coverage) > int(max_coverage):
        #         max_coverage = coverage.line_coverage

    from_new = 1

    # coverage_list = CoverageInfo.query.filter(CoverageInfo.gitlab_program_id == git_id,
    #                                           CoverageInfo.compare_branch == branch_name)
    # coverage_temp = dict()
    # for coverage in coverage_list:
    #     try:
    #         coverage_content = json.loads(coverage.content)
    #         service_name = coverage.service_name
    #         if service_name not in coverage_temp.keys():
    #             coverage_temp[service_name] = {"last_coverage": 0.0, "max_coverage": 0.0}
    #         if coverage.new_coverage == 0:
    #             if "content" in coverage_content[0].keys():
    #                 for content in coverage_content[0]["content"]:
    #                     if content["fileName"] == "total":
    #                         if float(content["filter_coverage"][:-1]) > 0:
    #                             coverage_temp[service_name]["last_coverage"] = float(content["filter_coverage"][:-1])
    #                             coverage_temp[service_name]["from_new"] = 0
    #                         if float(content["filter_coverage"][:-1]) > 0 and \
    #                                 float(content["filter_coverage"][:-1]) > \
    #                                 coverage_temp[service_name]["max_coverage"]:
    #                             coverage_temp[service_name]["max_coverage"] = float(content["filter_coverage"][:-1])
    #         elif coverage.new_coverage == 1:
    #             if coverage_content["lineCoverage"] >= 0:
    #                 coverage_temp[service_name]["last_coverage"] = coverage_content["lineCoverage"]
    #                 coverage_temp[service_name]["from_new"] = 1
    #             if coverage_content["lineCoverage"] >= 0 and \
    #                     coverage_content["lineCoverage"] > coverage_temp[service_name]["max_coverage"]:
    #                 coverage_temp[service_name]["max_coverage"] = coverage_content["lineCoverage"]
    #         else:
    #             pass
    #     except Exception as e:
    #         current_app.logger.error(e)
    #         send_tv(traceback.format_exc())
    #         send_tv("解析覆盖率报错：{0}".format(traceback.format_exc()))
    # last_coverage = max_coverage = 0.0
    # from_new = 0
    # for key, value in coverage_temp.items():
    #     if value["last_coverage"] > last_coverage:
    #         last_coverage = value["last_coverage"]
    #         max_coverage = value["max_coverage"]
    #         from_new = value["from_new"]
    return last_coverage, max_coverage, from_new, coverage_url


def get_date(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", hour=0, minute=0, second=0):
    return (datetime.now() + relativedelta(years=year, months=month, days=day,
                                           hours=hour, minutes=minute, seconds=second)).strftime(fmt)
