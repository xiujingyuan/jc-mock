#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/08/09
 @file: assumpt_task_view.py
 @site:
 @email:
"""
import math

from flask import current_app
from flask import render_template
from flask_login import login_required
from sqlalchemy import and_
from app.assumpt_task import task_assumpt
from app.base.views import BaseView
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.JenkinsJobDb import JenkinsJob
from app.models.KeyValueDb import KeyValue
from app.models.ProgramJenkinsDb import ProgramJenkin
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram
from app.models.TestEnvDb import TestEnv
import json
from datetime import datetime, timedelta

PAGE_COUNT = 15


@task_assumpt.route("/", methods=["GET"])
def index():
    return "Hello Assumpt Task!"


@task_assumpt.route("/test", methods=["GET"])
def test():
    return render_template(current_app.config["THEME_URL"] + "assumpt_task/index.html")


class LinkView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, program_id):
        program_ids = (3, 4, 16, 26) if program_id == 26 else (program_id,)
        program = SysProgram.query.filter(and_(SysProgram.sys_program_id == program_id,
                                               SysProgram.sys_is_active == 1)).first()

        assumpt_build_tasks = {}
        build_jenkins = {}
        test_env = {}

        program_total = {}

        # 获取第一页，每页15个的构建任务
        all_assumpt_tasks = AssumptBuildTask.query.filter(
            AssumptBuildTask.program_id.in_(program_ids),
            AssumptBuildTask.build_task_status == 1,
            AssumptBuildTask.mail_receive_time >= datetime.now() + timedelta(days=-90)).order_by(
            AssumptBuildTask.mail_receive_time.desc()).paginate(
            page=1,
            per_page=PAGE_COUNT,
            error_out=False)

        # 将任务状态，构建状态专成中文
        for all_assumpt_task in all_assumpt_tasks.items:
            if all_assumpt_task.last_build_status == 0:
                all_assumpt_task.change_last_build_status = "空闲"
            elif all_assumpt_task.last_build_status == 1:
                all_assumpt_task.change_last_build_status = "成功"
            elif all_assumpt_task.last_build_status == 2:
                all_assumpt_task.change_last_build_status = "失败"
            elif all_assumpt_task.last_build_status == 3:
                all_assumpt_task.change_last_build_status = "构建中"
            else:
                all_assumpt_task.change_last_build_status = "空闲"
        ret = []
        for item in all_assumpt_tasks.items:
            item.build_jenkins_jobs_str = json.loads(item.build_jenkins_jobs)
            ret.append(item.to_dict)
        print(json.dumps(ret))
        assumpt_build_tasks[program.sys_program_id] = all_assumpt_tasks.items

        # 获取买个项目对应的分页总数
        count = math.ceil(all_assumpt_tasks.total / PAGE_COUNT)
        program_total[program.sys_program_id] = count
        # 获取每个项目对应的环境ID

        test_env[program.sys_program_id] = []
        for program_item in program_ids:
            test_env[program_item] = []
            for env in TestEnv.query.filter(TestEnv.program_id == program_item).all():
                if env.env_id not in list(map(lambda x: x.env_id, test_env[program_item])):
                    test_env[program_item].append(env)
                if env.env_id not in list(map(lambda x: x.env_id, test_env[program.sys_program_id])):
                    test_env[program.sys_program_id].append(env)

            jenkins_job = JenkinsJob.query.filter(
                JenkinsJob.program_id == program_item).all()

            build_jenkins[program_item] = jenkins_job

        oa_modals = json.loads(KeyValue.query.filter(KeyValue.key == 'oa_modal_config').first().value)

        self.context.update({"assumpt_build_tasks": assumpt_build_tasks,
                             "program": program,
                             "test_env": test_env,
                             "build_jenkins": build_jenkins,
                             "program_total": program_total,
                             "mdm_url": current_app.config["MDM_URL"],
                             'oa_modals': oa_modals})

        return render_template(current_app.config["THEME_URL"] + 'assumpt_task/index.html', **self.context)


task_assumpt.add_url_rule('/<int:program_id>/', view_func=LinkView.as_view('task_assumpt'), methods=["GET"])
