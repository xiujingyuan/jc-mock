#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/03
 @file: view.py
 @site:
 @email:
"""
from flask import render_template
from flask_login import login_required

from app.base.views import BaseView
from app.models.AuthAssignmentDb import AuthItem
from app.models.MenuDb import Menu
from app.system import system


class RouteListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        routes = AuthItem.query.filter(AuthItem.type == 3).all()
        self.context.update({"routes": routes})
        return render_template(current_app.config["THEME_URL"] +'system/edit_auth_route.html', **self.context)


system.add_url_rule('/route/list', view_func=RouteListView.as_view('route_list'), methods=["GET"])


class PermissionListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        permissions = AuthItem.query.filter(AuthItem.type == 3).all()
        self.context.update({"permissions": permissions})
        return render_template(current_app.config["THEME_URL"] +'system/edit_auth_permission.html', **self.context)


system.add_url_rule('/permission/list', view_func=PermissionListView.as_view('permission_list'), methods=["GET"])


class MenuListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        level_menu = Menu.query.filter_by(parent=None).all()
        self.context.update({"level_menu": level_menu})
        return render_template(current_app.config["THEME_URL"] +'system/edit_auth_menu.html', **self.context)


system.add_url_rule('/menu/list', view_func=MenuListView.as_view('menu_list'), methods=["GET"])


# class MenuEditView(BaseView):
#     decorators = [login_required]
#
#     def dispatch_request(self):
#         menu_lists = Menu.query.all()
#         self.context.update({"menu_lists": menu_lists})
#         return render_template(current_app.config["THEME_URL"] +'system/edit_auth_menu.html', **self.context)
#
#
# system.add_url_rule('/menu/list', view_func=MenuEditView.as_view('menu_edit'), methods=["GET"])


class UserGroupListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
         return render_template(current_app.config["THEME_URL"] +'system/edit_user_group.html', **self.context)


system.add_url_rule('/user_group/list', view_func=UserGroupListView.as_view('user_group_list'), methods=["GET"])


class ProgramListView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] +'system/edit_program.html', **self.context)


system.add_url_rule('/program/list', view_func=ProgramListView.as_view('program_list'), methods=["GET"])

