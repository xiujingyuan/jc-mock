#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/18
 @file: system_api.py
 @site:
 @email:
"""
from app.api.case.case_api import get_sys_program
from app.tools.tools import send_tv
from kubernetes import client, config
import os

from app import db
from app.api.system import api_system
from flask import Flask, jsonify, request, current_app, Response
from flask_login import current_user

from app.common.models import model_to_dict
from app.models.AuthAssignmentDb import AuthItem
from app.models.MenuDb import Menu
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram


@api_system.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello System!'


@api_system.route('/permission/', methods=['POST', 'PUT', 'GET', "DEL"])
def permission():
    """
    创建权限，更新权限，删除权限
    :return:
    """
    if request.method == "GET":
        json_data = request.args
        page_index = int(json_data["page_index"])
        page_size = int(json_data["page_size"])
        permissions = AuthItem.query.filter(AuthItem.type == 3).paginate(page=page_index, per_page=page_size, error_out=False)
        permission_info = []
        for permission_item in permissions.items:
            permission_info.append(model_to_dict(permission_item))
        print(permission_info)
        query_ret = {"total": permissions.total, "rows": permission_info}
        return jsonify(query_ret)


@api_system.route('/menu/', methods=['POST', 'PUT', 'GET', "DEL"])
def menu():
    """
    创建菜单，更新菜单，删除菜单
    :return:
    """
    if request.method == "GET":
        json_data = request.args
        page_index = int(json_data["page_index"])
        page_size = int(json_data["page_size"])
        menus = Menu.query.paginate(page=page_index, per_page=page_size, error_out=False)
        menu_info = []
        for menu_item in menus.items:
            menu_dict = model_to_dict(menu_item)
            menu_dict["parent"] = Menu.query.filter_by(id=menu_dict["parent"]).first().name if \
                menu_dict["parent"] else "-"
            menu_info.append(menu_dict)
        query_ret = {"total": menus.total, "rows": menu_info}
        return jsonify(query_ret)


@api_system.route('/user_group/', methods=['POST', 'PUT', 'GET', "DEL"])
def user_group():
    """
    创建用户组，更新用户组，删除用户组
    :return:
    """
    if request.method == "GET":
        user_groups = SysOrganization.query.all()
        user_group_info = []
        for user_group_item in user_groups:

            parent_name = SysOrganization.query.filter(
                SysOrganization.sys_organization_id ==
                user_group_item.sys_organization_id).first().sys_organization_name \
                if user_group_item.sys_organization_parent_id else "-"
            user_group_dict = model_to_dict(user_group_item)
            user_group_dict.update({"parent_name": parent_name})
            user_group_info.append(user_group_dict)
        query_ret = {"total": len(user_groups), "rows": user_group_info}
        return jsonify(query_ret)


@api_system.route('/program/', methods=['POST', 'PUT', 'GET', "DEL"])
def program():
    """
    创建项目，更新项目，删除项目
    :return:
    """
    if request.method == "GET":
        programs = SysProgram.query.all()
        program_info = []
        for program_item in programs:
            organization = SysOrganization.query.filter(SysOrganization.sys_organization_id == program_item.sys_program_group_id).first()
            organization = "未找到" if organization is None else organization.sys_organization_name
            program_item_dict = model_to_dict(program_item)
            program_item_dict.update({"sys_program_group_name": organization})
            program_info.append(program_item_dict)
        query_ret = {"total": len(programs), "rows": program_info}
        return jsonify(query_ret)


@api_system.route('/kill', methods=['POST', 'PUT', 'GET', "DEL"])
def kill():
    """
    重启系统
    :return:
    """
    os.popen("killall5")


@api_system.route('/restart', methods=['POST', 'PUT', 'GET', "DEL"])
def restart():
    """
    重启系统
    :return:
    """
    cur_dir = os.getcwd()
    config_file = os.path.join(cur_dir, "environment/k8s/kube_config")
    print(config_file)
    config.kube_config.load_kube_config(config_file=config_file)
    core_api = client.CoreV1Api()
    pod_list = core_api.list_namespaced_pod("biz")
    pod_name = ""
    for pod in pod_list.items:
        if "app" in pod.metadata.labels.keys() and pod.metadata.labels["app"] == "test-platform":
            pod_name = pod.metadata.name
    send_tv("服务重启，%s已经重启服务，删一个pod名:%s" % (current_user.username, pod_name))
    core_api.delete_namespaced_pod(pod_name, "biz")


@api_system.route('/reset_redis_key/<string:key>', methods=['GET'])
def reset_redis_key(key):
    current_app.app_redis.delete(key)
    if key == "jc-sys_programs":
        get_sys_program()
    return jsonify()


if __name__ == "__main__":
    restart()
