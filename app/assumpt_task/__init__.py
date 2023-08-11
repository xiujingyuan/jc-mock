#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/08/09
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

task_assumpt = Blueprint('task_assumpt', __name__)

from . import assumpt_task_view
