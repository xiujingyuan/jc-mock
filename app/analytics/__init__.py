#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/03/29
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
url_analytics = Blueprint('analytics', __name__)

from . import analytics
