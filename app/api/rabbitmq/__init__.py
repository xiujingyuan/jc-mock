#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/17
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint

api_rabbitmq = Blueprint('api_rabbitmq', __name__)

from . import view
