#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: zhushasha
 @software: PyCharm
 @time: 2020/11/13
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

view_int = Blueprint('int', __name__)

from . import int_view
