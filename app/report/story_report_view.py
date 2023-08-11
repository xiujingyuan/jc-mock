#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/11
 @file: sotry_report.py
 @site:
 @email:
"""

import json
from datetime import datetime

from flask import current_app
from flask import render_template
from flask_login import login_required
from sqlalchemy import and_
import time

from app import db
from app.base.views import BaseView
from app.common.Tapd import get_current_iteration
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram
from app.models.TapdKeyValueDb import TapdKeyValue
from app.report import view_report
import requests


class ReportView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'report/index.html', **self.context)


view_report.add_url_rule('/', view_func=ReportView.as_view('report'), methods=["GET"])


class ReportSetView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        program_works = SysProgram.query.filter(and_(SysProgram.sys_is_active == 1,
                                                     SysProgram.tapd_work_ids.like("[%]"))).all()
        program = []
        iteration = []
        current_iteration_dict = {}
        end_time = datetime.now().date()
        for work in program_works:

            work_id = work.tapd_work_ids[1:-1]
            program.append({
                "name": work.sys_program_name,
                "work_id": work_id,
            })
            find_item = TapdKeyValue.query.filter(and_(
                TapdKeyValue.key == "tapd_info",
                TapdKeyValue.type == "iteration",
                TapdKeyValue.workspace_id == work_id)).first()
            if find_item is not None:
                iteration_info = json.loads(find_item.value)
                work_id_info = get_iterations(work_id, iteration_info, current_iteration_dict, end_time)
                iteration.append(work_id_info)

        self.context.update({
            "program_works": program,
            "iteration": iteration
        })
        return render_template(current_app.config["THEME_URL"] + 'report/setting.html', **self.context)


view_report.add_url_rule('/setting', view_func=ReportSetView.as_view('report_setting'), methods=["GET"])


class ReportTrendView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'report/trend.html', **self.context)


view_report.add_url_rule('/trend', view_func=ReportTrendView.as_view('report_trend'), methods=["GET"])


class ProgramReportTrendView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, origination):
        origination_name = SysOrganization.query.filter_by(sys_organization_id=origination).one()
        origination_name = origination_name.sys_organization_name if origination_name else '未找到'
        programs = SysProgram.query.filter(and_(SysProgram.sys_program_group_id == origination,
                                                SysProgram.sys_is_active == 1,
                                                SysProgram.sys_program_id != 25)).all()

        if programs and len(programs) == 1 and programs[0].sys_program_name == '基础系统':
            programs = SysProgram.query.filter(SysProgram.sys_program_group_id == 1,
                                                    SysProgram.sys_is_active == 0).all()
        program_ids = list(map(lambda x: x.sys_program_id, programs))
        iteration = []
        current_iteration_dict = {}
        end_time = datetime.now().date()
        for program in programs:
            if program.tapd_work_ids is None:
                continue
            work_id = program.tapd_work_ids[1:-1]
            find_item = TapdKeyValue.query.filter(and_(
                TapdKeyValue.key == "tapd_info",
                TapdKeyValue.type == "iteration",
                TapdKeyValue.workspace_id == work_id)).first()
            if find_item is not None:
                iteration_info = json.loads(find_item.value)
                work_id_info = get_iterations(work_id, iteration_info, current_iteration_dict, end_time)
                iteration.append(work_id_info)

        self.context.update({"programs": programs,
                             "program_ids": program_ids,
                             "iteration": iteration,
                             "current_iterations": current_iteration_dict,
                             "origination_name": origination_name,
                             "origination": origination})

        return render_template(current_app.config["THEME_URL"] + 'report/program_report.html', **self.context)


view_report.add_url_rule('/<int:origination>/', view_func=ProgramReportTrendView.as_view('report_program'),
                         methods=["GET"])


def get_iterations(work_id, iteration_info, current_iteration_dict, end_time):
    iteration_info_list = list(map(lambda x: {"id": x["id"],
                                              "name": x["name"],
                                              "startdate": x["startdate"]}, iteration_info))
    sorted_iteration_info = sorted(iteration_info_list, key=lambda x: x["startdate"], reverse=True)
    current_iteration = get_current_iteration(work_id, end_time)
    current_iteration_index = list(map(lambda x: x["id"], sorted_iteration_info)).index(current_iteration) \
        if current_iteration else -1
    if current_iteration:
        current_iteration_dict[work_id] = current_iteration
    if len(sorted_iteration_info) <= 6:
        work_id_info = {work_id: sorted_iteration_info}
    elif current_iteration_index == -1:
        work_id_info = {work_id: sorted_iteration_info[0: 6]}
    elif current_iteration_index < 3:
        work_id_info = {work_id: sorted_iteration_info[0: 6]}
    elif current_iteration_index >= len(sorted_iteration_info) - 3:
        work_id_info = {work_id: sorted_iteration_info[-6: -1]}
    else:
        work_id_info = {work_id: sorted_iteration_info[current_iteration_index - 3:
                                                       current_iteration_index + 3]}
    return work_id_info


class TestView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'index2.html', **self.context)


view_report.add_url_rule('/test2', view_func=TestView.as_view('report_index2'), methods=["GET"])


class AddView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'cases.html', **self.context)


view_report.add_url_rule('/add', view_func=AddView.as_view('report_add'), methods=["GET"])


class UserListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'userList.html', **self.context)


view_report.add_url_rule('/userList', view_func=UserListView.as_view('report_userList'), methods=["GET"])


class CheckBoxView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'checkbox.html', **self.context)


view_report.add_url_rule('/checkbox', view_func=CheckBoxView.as_view('report_checkbox'), methods=["GET"])

