# @Time    : 2019/12/13 7:19 下午
# @Author  : yuanxiujing
# @File    : dh_tool.py
# @Software: PyCharm
from flask import render_template, current_app
import json
from flask_login import login_required
from app.base.views import BaseView
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram
from app.models.KeyValueDb import KeyValue
from app.tool_set import tool_set
from sqlalchemy import and_


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

        asset_from_app = KeyValue.query.filter_by(key="sync_from_app_list").first()
        asset_from_app = json.loads(asset_from_app.value) if asset_from_app is not None else []

        self.context.update({"from_app": asset_from_app})
        self.context.update({"origination_name": origination_name})

        return render_template(current_app.config["THEME_URL"] +'tool_set/dh/dh_tool.html', **self.context)


tool_set.add_url_rule('dh/<int:organization>/', view_func=OrganizationToolView.as_view('organization_tool'),
                      methods=["GET"])

