#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/09
 @file: task_view.py
 @site:
 @email:
"""
from flask import jsonify
from app.tasks import task_url
from app.tasks.search_story.search_story_task import get_for_test


@task_url.route("/get_for_test", methods=["GET"])
def get_for_test_task():
    get_for_test.delay()
    return jsonify({"code": "success"})
