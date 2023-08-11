#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/10/22
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_tapd = Blueprint('api_tapd', __name__)

from . import tapd_api
