#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/04/03
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

system = Blueprint('system', __name__)

from . import permission
