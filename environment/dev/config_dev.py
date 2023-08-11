#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/18
 @file: config.py
 @site:
 @email:
"""
from environment.common.config import Config
import os


class DevelopmentConfig(Config):
    DEBUG = True
    DOMAIN = "http://127.0.0.1:5102"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3306/jc-mock?charset=utf8'
    SQLALCHEMY_BINDS = {
        "dh": 'mysql+pymysql://root:root@127.0.0.1:3307/qsq_fox?charset=utf8',
        "jihe": 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3317/dh_jihe?charset=utf8',
        "tmms": 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3317/tmms?charset=utf8',
        "oa": 'mysql+pymysql://root:V5M)wOdX2^OE@127.0.0.1:3318/kn.oa2-testing.kuainiujinke.com?charset=utf8',
        "qnn": 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3317/qnn_clearing2?charset=utf8',
        "rbiz1": 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3317/rbiz1?charset=utf8',
        "rbiz2": 'mysql+pymysql://root:Coh8Beyiusa7@127.0.0.1:3317/rbiz2?charset=utf8',
    }
    # PASSPORT_HEADER = "https://stage-oa.kuainiu.io/account"
    PASSPORT_CLIEND_ID = 18
    PASSPORT_CLIENT_SECRET = "AuSWC6sRk0ZgZeeqkzxNZsqtQZE9ZjGXRmpyXSBl"
    PASSPORT_CALLBACK_URL = "http://127.0.0.1:5102/auth/kuainiu/user/auth?authclient=kuainiu"

    PASSPORT_VUE_CLIEND_ID = 306
    PASSPORT_VUE_CLIENT_SECRET = "trSIpvAIq4w9ShRrOUxuRcuXi0jhvGAHc7JZNmgd"
    PASSPORT_VUE_CALLBACK_URL = "http://127.0.0.1:3001/auth/callback"

    SENTRY_DSN = "https://c825ef551d3045029ceb90799f894286:5e5ed9ee34754bbebb1494cc79679e25@sentry.kuainiujinke.com/230"

    BACKEND_URL = "http://127.0.0.1:5102"
    REDIRECT_URL = 'http://127.0.0.1:3001/'

    # websocket的请求地址
    MDM_URL = "http://127.0.0.1:5000/"

    FILE_HOME = os.getcwd()
    # celery
    BROKER_URL = "redis://:123456@localhost:6379/6"
    CELERY_RESULT_BACKEND = "redis://:123456@localhost:6379/7"

    ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': 'redis://:123456@localhost:6379/5',
            'default_timeout': 5
        }
    }

    # CELERY_REDIS_SCHEDULER_URL = "redis://:123456@localhost:6379/8"

    # Jenkins run case 配置
    JENKINS_RUN_JOB = ["Auto_Test_Api_Run_Case_Debug", "Auto_Test_Api_Run_Case_Debug_1"]
