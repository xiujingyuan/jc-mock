#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/17
 @file: view.py
 @site:
 @email:
"""
import json

import requests
from flask import current_app, jsonify, request

from app import csrf
from app.api.rabbitmq import api_rabbitmq


@api_rabbitmq.route("/", methods=["GET"])
def hello_world():
    return "Hello rabbitmq"


@api_rabbitmq.route("/sms", methods=["POST"])
@csrf.exempt
def sms_pulish():
    rabbitmq_publish_url = "{0}{1}".format(current_app.config["RABBITMQ_HOST"], current_app.config["RABBITMQ_URL"])
    header = {
        "username": current_app.config["RABBITMQ_USERNAME"],
        "token": current_app.config["RABBITMQ_PASSWORD"],
        "Content-Type": "application/json"
    }
    req_data = request.json

    report_callback = {
        "topicName": "sms-request-notice",
        "data": req_data,
        "tagList": ["fox", "wyapp"],
        "delayTime": "1"
    }
    ret = requests.post(rabbitmq_publish_url, data=json.dumps(report_callback), headers=header)
    return jsonify(ret.json())


@api_rabbitmq.route("/call", methods=["POST"])
@csrf.exempt
def call_pulish():
    rabbitmq_publish_url = "{0}{1}".format(current_app.config["RABBITMQ_HOST"], current_app.config["RABBITMQ_URL"])
    header = {
        "username": current_app.config["RABBITMQ_USERNAME"],
        "token": current_app.config["RABBITMQ_PASSWORD"],
        "Content-Type": "application/json"
    }
    req_data = request.json

    report_callback = {
        "topicName": "call-request-notice",
        "data": req_data,
        "tagList": ["fox", "wyapp"],
        "delayTime": "1"
    }
    ret = requests.post(rabbitmq_publish_url, data=json.dumps(report_callback), headers=header)
    return jsonify(ret.json())



