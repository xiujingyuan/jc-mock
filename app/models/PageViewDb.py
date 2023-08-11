#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/03/29
 @file: PageViewDb.py
 @site:
 @email:
"""
from urllib.parse import urlparse, parse_qsl

from app import db
from datetime import datetime
from flask import request


class PageView(db.Model):
    __tablename__ = 'page_views'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255))
    url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(255), default='')
    ip = db.Column(db.String(255), default='')
    referrer = db.Column(db.String(255), default='')
    user_agent = db.Column(db.String(255), default='')
    headers = db.Column(db.JSON)
    params = db.Column(db.JSON)


    @classmethod
    def create_from_request(cls):
        page_view = PageView()
        parsed = urlparse(request.args['url'])
        params = dict(parse_qsl(parsed.query))
        user_agent = request.user_agent

        page_view.domain = parsed.netloc,
        page_view.url = parsed.path,
        page_view.title = request.args.get('t') or '',
        page_view.ip = request.headers.get('X-Forwarded-For', request.remote_addr),
        page_view.referrer = request.args.get('ref') or '',
        page_view.user_agent = request.user_agent.browser,
        page_view.headers = dict(request.headers),
        page_view.params = params

        db.session.add(page_view)
        db.session.flush()
