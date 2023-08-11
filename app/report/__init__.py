#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/11
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

view_report = Blueprint('report', __name__)

from . import story_report_view
