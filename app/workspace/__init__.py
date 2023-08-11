#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2020/08/10
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

view_workspace = Blueprint('workspace', __name__)

from . import workspace_view
