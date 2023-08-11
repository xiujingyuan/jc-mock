#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/01/23
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_case = Blueprint('api_case', __name__)

from . import case_api
