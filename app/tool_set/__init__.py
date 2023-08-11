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

tool_set = Blueprint('tool_set', __name__)

from . import basic_tools
