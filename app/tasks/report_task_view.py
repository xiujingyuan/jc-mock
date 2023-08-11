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
from app.tasks.test_report.report_task import get_story_data, get_bug_map, get_story_map, \
    get_iteration_map, get_workspace_info, get_bug_data, get_git_tag_data, get_iteration_data, \
    get_sonar_data, get_case_data, get_test_plan_data, get_git_merge_data, get_relation_data, get_story_fields_info


@task_url.route("/get_story_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_story_data_task(program_id, query_start_time, query_month):
    get_story_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_test_plan_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_test_plan_data_task(program_id, query_start_time, query_month):
    get_test_plan_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_case_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_case_data_task(program_id, query_start_time, query_month):
    get_case_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_bug_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_bug_data_task(program_id, query_start_time, query_month):
    get_bug_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_git_commit_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_git_merge_data_task(program_id, query_start_time, query_month):
    get_git_merge_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_git_tag_data/<int:program_id>/<string:query_start_time>/<string:query_month>", methods=["GET"])
def get_git_tag_data_task(program_id, query_start_time, query_month):
    get_git_tag_data.apply_async(args=[program_id, query_start_time, query_month])
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_sonar_data", methods=["GET"])
def get_sonar_data_task():
    get_sonar_data.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_bug_map/", methods=["GET"])
def get_bug_map_task():
    get_bug_map.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_story_map/", methods=["GET"])
def get_story_map_task():
    get_story_map.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_story_fields_info/", methods=["GET"])
def get_story_fields_info_task():
    get_story_fields_info.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_iteration_map/", methods=["GET"])
def get_iteration_map_task():
    get_iteration_map.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_iteration_data/", methods=["GET"])
def get_iteration_data_task():
    get_iteration_data.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_workspace_info/", methods=["GET"])
def get_workspace_info_task():
    get_workspace_info.delay()
    return jsonify({"code": 0,
                    "message": "success"})


@task_url.route("/get_relation_data/", methods=["GET"])
def get_relation_data_task():
    get_relation_data.delay()
    return jsonify({"code": 0,
                    "message": "success"})
