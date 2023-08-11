#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/27
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
mock = Blueprint('mock', __name__)

from . import mock_api
