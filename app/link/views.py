#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/23
 @file: views.py
 @site:
 @email:
"""

from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app
from flask_login import login_required, current_user

from app import db
from app.base.views import BaseView
from app.link import link
from app.models.LinkModel import Link
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram


@link.route('/link/', methods=['GET'])
def hello_world():
    return 'Hello link!'


class LinkView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, origination):
        organizations = SysOrganization.query.filter_by(sys_organization_parent_id=origination).all()
        origination_name = SysOrganization.query.filter_by(sys_organization_id=origination).one()

        origination_name = origination_name.sys_organization_name if origination_name else '未找到'
        organizations = tuple(map(lambda x: x.sys_organization_id, organizations)) if organizations else (origination, )
        programs = SysProgram.query.filter(SysProgram.sys_program_group_id.in_(organizations)).all()
        link_urls = {}
        for program in programs:
            link_urls[program.sys_program_id] = Link.query.filter_by(link_type=program.sys_program_id).all()

        self.context.update({"link_urls": link_urls, "programs": programs, "origination_name": origination_name})
        return render_template(current_app.config["THEME_URL"] +'link.html', **self.context)


link.add_url_rule('/link/<int:origination>/', view_func=LinkView.as_view('link'), methods=["GET"])
