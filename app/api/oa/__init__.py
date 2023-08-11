#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/04
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_oa = Blueprint('api_oa', __name__)

from . import oa_api
