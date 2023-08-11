#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/03/18
 @file: errors.py
 @site:
 @email:
"""

import traceback

from flask import jsonify, request, Response
import json
from app import db
from app.models.ApiLogDb import Apilog
from app.models.ErrorLogs import ErrorLogs


def catch_error(error_type):
    def wrapper(func):
        """
        捕获异常并写入到数据库中
        :param func:
        :return:
        """
        def inner_wrapper(*args, **kwargs):
            try:
                data = None
                ret = None
                print("method", request.method)
                print("host", request.host)
                print("base_url", request.path)
                data = request.json
                ret = func(*args, **kwargs)
            except:
                data = {
                    "code": 1,
                    "message": "查询错误"
                    }
                ret = jsonify(data) if error_type == "api" else None
                error_log = ErrorLogs()
                error_log.error_log_msg = traceback.format_exc()
                db.session.add(error_log)
                db.session.flush()
            finally:
                if error_type == "api":
                    api_log = Apilog()
                    api_log.apilog_method = request.method
                    api_log.apilog_servername = request.host
                    api_log.apilog_response_body = json.dumps(json.loads(ret.data.decode("utf8"))) if \
                        isinstance(ret, Response) else "返回错误"
                    api_log.apilog_request_body = request.data if data is None else data
                    api_log.apilog_url = request.path
                    db.session.add(api_log)
                    db.session.flush()
                return ret
        return inner_wrapper
    return wrapper

