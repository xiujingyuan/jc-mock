#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/24
 @file: __init__.py.py
 @site:
 @email:
"""
from flask import Blueprint
api_contract = Blueprint('api_contract', __name__)

from . import contract_api
