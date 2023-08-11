#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/05
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_setting = Blueprint('api_setting', __name__)

from . import setting_api
