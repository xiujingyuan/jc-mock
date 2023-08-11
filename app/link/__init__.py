#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/23
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Blueprint

link = Blueprint('link', __name__)

from . import views
