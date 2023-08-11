#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/18
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_system = Blueprint('api_system', __name__)

from . import system_api
