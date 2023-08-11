#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/22
 @file: views.py
 @site:
 @email:
"""
import json

import sqlalchemy
from flask import views, current_app
from sqlalchemy import and_

from app.models.MenuDb import Menu
from app.models.ProgramBusinessDb import ProgramBusiness
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram


class BaseView(views.View):
    def __init__(self):
        super(BaseView, self).__init__()
        if current_app.app_redis.exists("jc-mock_menus"):
            menus = json.loads(current_app.app_redis.get("jc-mock_menus"))
        else:
            menus = Menu.query.filter(and_(Menu.parent.is_(None),
                                           Menu.is_active == 1)).order_by(Menu.order.asc()).all()
            menus = list(map(lambda x: x.serialize(), menus))
            current_app.app_redis.set("jc-mock_menus", json.dumps(menus))

        if current_app.app_redis.exists("jc-mock_child_menus"):
            child_menus = json.loads(current_app.app_redis.get("jc-mock_child_menus"))
        else:
            child_menus = {}
            for menu in menus:
                menu["route"] = menu["route"] if menu["route"] is not None else '#'
                child_menus[str(menu["id"])] = []
                for child_menu in Menu.query.filter_by(parent=menu["id"], is_active=1).order_by(Menu.order.asc()).all():
                    child_menu.route = child_menu.route if child_menu.route is not None else '#'
                    child_menus[str(menu["id"])].append(child_menu.serialize())
            current_app.app_redis.set("jc-mock_child_menus", json.dumps(child_menus))

        if current_app.app_redis.exists("jc-sys_organizations"):
            sys_organizations = json.loads(current_app.app_redis.get("jc-sys_organizations"))
        else:
            sys_organizations = SysOrganization.query.filter(and_(
                SysOrganization.sys_organization_parent_id.is_(None),
                SysOrganization.sys_del_flag == 0)).all()
            sys_organizations = list(map(lambda x: x.serialize(), sys_organizations))
            for item in sys_organizations:
                item.pop("sys_organizations")
            current_app.app_redis.set("jc-sys_organizations", json.dumps(sys_organizations))

        if current_app.app_redis.exists("jc-sys_programs"):
            sys_programs = json.loads(current_app.app_redis.get("jc-sys_programs"))
        else:
            sys_programs = SysProgram.query.filter(SysProgram.sys_is_active == 1).all()
            sys_programs = list(map(lambda x: x.serialize(), sys_programs))
            for sys_pro in sys_programs:
                sys_pro["sys_organization"] = sys_pro["sys_organization"].serialize()
                sys_pro["sys_organization"].pop("sys_organizations")
            current_app.app_redis.set("jc-sys_programs", json.dumps(sys_programs))

        if current_app.app_redis.exists("jc-program_business"):
            program_business = json.loads(current_app.app_redis.get("jc-program_business"))
        else:
            program_business = []
            for sys_pro in sys_programs:
                program_id = sys_pro["sys_program_id"]
                program_businesses = ProgramBusiness.query.filter(ProgramBusiness.program_id
                                                                  == program_id).all()
                program_business.append({program_id: ProgramBusiness.serialize_list(program_businesses)})
            current_app.app_redis.set("jc-program_business", json.dumps(program_business))

        cdn_host = current_app.config["CDN_HOST"]

        self.context = {"menus": menus,
                        "child_menus": child_menus,
                        "sys_programs": sys_programs,
                        "program_business": program_business,
                        "sys_organizations": sys_organizations,
                        "cdn_host": cdn_host}
