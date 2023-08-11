#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/24
 @file: contract_api.py
 @site:
 @email:
"""
from app.api.contract import api_contract
from flask import request, current_app, jsonify


@api_contract.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Contract!'


@api_contract.route('/callback', methods=['GET', 'POST'])
def callback():
    ret = request.json
    ret1 = request.data
    ret2 = request.args
    ret3 = request.headers
    ret4 = request.form
    current_app.logger.info(ret)
    current_app.logger.info(ret1)
    current_app.logger.info(ret2)
    current_app.logger.info(ret3)
    current_app.logger.info(ret4)
    return jsonify({})
