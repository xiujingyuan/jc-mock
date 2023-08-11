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

task_url = Blueprint('tasks', __name__)

from . import task_view, build_task_view, search_story_task_view, coverage_task_view, report_task_view, run_pipeline_view, sonar_schedule_view

# def make_celery(app):
#     celery = Celery(app.import_name,
#                     backend=app.config["CELERY_RESULT_BACKEND"],
#                     broker=app.config["CELERY_BROKER_URL"])
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery



