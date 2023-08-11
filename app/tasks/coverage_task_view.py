#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/04
 @file: coverage_task_view.py
 @site:
 @email:
"""
from flask import jsonify

from app.tasks import task_url
from app.tasks.coverage_task.coverage_task import get_diff_coverage_new


@task_url.route("/get_diff_coverage_new", methods=["GET"])
def get_coverage_new():
    get_diff_coverage_new.delay()
    return jsonify({"code": 0,
                    "message": "success"})
