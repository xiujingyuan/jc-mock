#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/05
 @file: tmms_tools.py
 @site:
 @email:
"""
import traceback
import urllib
from flask import render_template, current_app
import json
from flask_login import login_required
from sqlalchemy import and_

from app.base.views import BaseView
from app.common.Serializer import Serializer
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram
from app.models.KeyValueDb import KeyValue
from app.models.CommonToolsDb import CommonTool
from app.tool_set import tool_set


class OrganizationToolView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, organization):
        organizations = SysOrganization.query.filter_by(sys_organization_parent_id=organization).all()

        origination_name = SysOrganization.query.filter_by(sys_organization_id=organization).one()
        origination_name = origination_name.sys_organization_name if origination_name else '未找到'

        organizations = tuple(map(lambda x: x.sys_organization_id, organizations)) if organizations else (organization,)
        programs = SysProgram.query.filter(and_(
            SysProgram.sys_program_group_id.in_(organizations),
            SysProgram.sys_is_active == 1)).all()
        self.context.update({"programs": programs})

        from_system = Keyvalue.query.filter_by(keyvalue_key="task_from_system_list").first()
        from_system = json.loads(from_system.keyvalue_value) if from_system is not None else []

        customer_channel = Keyvalue.query.filter_by(keyvalue_key="customer_channel_list").first()
        customer_channel = json.loads(customer_channel.keyvalue_value) if customer_channel is not None else []

        self.context.update({"from_systems": from_system})
        self.context.update({"customer_channels": customer_channel})

        check = current_app.create_task if hasattr(current_app, "create_task") else False

        self.context.update({"check": check})
        self.context.update({"origination_name": origination_name})

        dh_from_app = KeyValue.query.filter_by(key="sync_from_app_list").first()
        dh_from_app = json.loads(dh_from_app.value) if dh_from_app is not None else []

        self.context.update({"dh_from_app": dh_from_app})
        self.context.update({"origination_name": origination_name})

        case = None
        try:
            get_case = urllib.request.urlopen('{0}/common/tools'.format(current_app.config["BACKEND_URL"]))
            print(current_app.config["BACKEND_URL"])
            # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
            result = get_case.read()

        except:
            current_app.logger.exception(traceback.format_exc())
            pass
        else:
            json_result = json.loads(result)

            if "code" in json_result and "data" in json_result:
                if json_result["code"] == 0:
                    if json_result["data"] is not None:
                        case = json_result["data"]
        self.context.update({"tools": case})

        return render_template(current_app.config["THEME_URL"] + 'tool_set/basic_tools.html', **self.context)


tool_set.add_url_rule('/<int:organization>/', view_func=OrganizationToolView.as_view('organization_tool'), methods=["GET"])




class ToolHomeView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        organizations = SysOrganization.query.filter(SysOrganization.sys_del_flag == 0).all()
        programs_dict = {}
        for org in organizations:
            programs = SysProgram.query.filter(and_(
                SysProgram.sys_program_group_id == org.sys_organization_id,
                SysProgram.sys_is_active == 1)).all()
            programs_dict[org.sys_organization_name] = Serializer.serialize_list(programs)

        self.context.update({"org_programs": programs_dict})
        from_system = KeyValue.query.filter(KeyValue.key == "task_from_system_list").first()
        from_system = json.loads(from_system.keyvalue_value) if from_system is not None else []

        customer_channel = KeyValue.query.filter(KeyValue.key == "customer_channel_list").first()
        customer_channel = json.loads(customer_channel.keyvalue_value) if customer_channel is not None else []

        self.context.update({"from_systems": from_system})
        self.context.update({"customer_channels": customer_channel})

        check = current_app.create_task if hasattr(current_app, "create_task") else False

        self.context.update({"check": check})

        from_app = KeyValue.query.filter(KeyValue.key=="sync_from_app_list").first()
        from_app = json.loads(from_app.value) if from_app is not None else []

        self.context.update({"dh_from_app": from_app})

        get_all_common = CommonTool.query.all()
        get_all_common_json = Serializer.serialize_list(get_all_common)
        self.context.update({"tools": get_all_common_json})

        return render_template(current_app.config["THEME_URL"] + 'tool_set/basic_tools.html', **self.context)


tool_set.add_url_rule('/', view_func=ToolHomeView.as_view('tool_home'), methods=["GET"])
