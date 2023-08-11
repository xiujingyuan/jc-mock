#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/26
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Blueprint
api_statistics_report = Blueprint('api_statistics_report', __name__)

from . import statistics_report_api
