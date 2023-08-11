#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/09/05
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_coverage = Blueprint('api_coverage', __name__)

from . import coverage_api
