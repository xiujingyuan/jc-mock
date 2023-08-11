#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/03/29
 @file: analytics.py
 @site:
 @email:
"""
from flask import Response, request, abort, current_app
from app.analytics import url_analytics
from app.models.PageViewDb import PageView


@url_analytics.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Case!'


@url_analytics.route('/a.gif')
def analyze():
    # TODO: implement 1pixel gif view.
    if not request.args.get('url'):
        abort(404)

    PageView.create_from_request()

    my_response = Response(current_app.config['BEACON'], mimetype='image/gif')
    my_response.headers['Cache-Control'] = 'private, no-cache'
    return my_response


@url_analytics.route('/a.js')
def script():
    # TODO: implement javascript view.
    return Response(
        current_app.config['JAVASCRIPT'] % (current_app.config['DOMAIN']),
        mimetype='text/javascript')
