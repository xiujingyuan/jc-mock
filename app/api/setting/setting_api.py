#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/05
 @file: setting_api.py
 @site:
 @email:
"""
from app.api.setting import api_setting
from flask import Flask, jsonify, request, current_app, Response

from app.common.models import model_to_dict
from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram


@api_setting.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Setting!'


