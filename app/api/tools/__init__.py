#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/07
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_tools = Blueprint('api_tools', __name__)

from . import tmms_tools
