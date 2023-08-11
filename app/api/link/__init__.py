#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/30
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_link = Blueprint('api_link', __name__)

from . import link_api
