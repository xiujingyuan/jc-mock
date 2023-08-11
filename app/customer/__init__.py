#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/12/18
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Blueprint

customer = Blueprint('customer', __name__)

from . import forms, views
from ..models.PermissionModel import Permission


@customer.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
