#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/08/15
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Blueprint
api_build_task = Blueprint('api_build_task', __name__)

from . import build_task_api
