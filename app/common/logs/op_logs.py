#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/02/22
 @file: op_logs.py
 @site:
 @email:
"""
from app import db
from app.models.ApiLogDb import Apilog


def write_api_log():
    apilog = Apilog()
    apilog.apilog_request_at = ""
    apilog.apilog_request_body = ""
    apilog.apilog_url = ""
    apilog.apilog_create_at = ""
    apilog.apilog_method = ""
    apilog.apilog_response_body = ""
    
