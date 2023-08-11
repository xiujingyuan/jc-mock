#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/12/20
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Blueprint
tmms = Blueprint('tmms', __name__)

from . import tmms_api