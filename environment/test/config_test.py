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


class TestingConfig(Config):
    # TESTING = True
    DEBUG = False
    DOMAIN = "http://testing-platform.kuainiu.io"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/jc-mock?charset=utf8'
    SQLALCHEMY_BINDS = {
        "dh": 'mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/qsq_fox?charset=utf8',
        "jihe": 'mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/dh_jihe?charset=utf8',
        "tmms": 'mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/tmms?charset=utf8',
        "oa": 'mysql+pymysql://aa10.aa.test:oa10test123456@10.1.5.14:3306/kn.oa2-testing.kuainiujinke.com?charset=utf8',
        "qnn": 'mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/qnn_clearing2?charset=utf8'
    }
    WTF_CSRF_ENABLED = False

    PASSPORT_VUE_CLIEND_ID = 345
    PASSPORT_VUE_CLIENT_SECRET = "GEHSyXWST6HFl0cGL9DU7V43RrSK0gQ7FERoABjV"
    PASSPORT_VUE_CALLBACK_URL = "https://auto-vue.k8s-ingress-nginx.kuainiujinke.com/auth/callback"
    REDIRECT_URL = 'https://auto-vue.k8s-ingress-nginx.kuainiujinke.com/'

    PASSPORT_CLIEND_ID = 21
    PASSPORT_CLIENT_SECRET = "RyhQohc2y1w2Y40uCBheKNWZfb4kZszXphNlHTLp"
    PASSPORT_CALLBACK_URL = "http://testing-platform.kuainiu.io/auth/kuainiu/user/auth?authclient=kuainiu"
    SENTRY_DSN = "https://47a43c1e88cb4c4d8d193aac9dac05bc:9c326700cec14d32920e84b2b7ab4492@sentry.kuainiujinke.com/229"

    REDIS_HOST = "redis-svc"
    REDIS_PORT = "6379"
    REDIS_PWD = "kuainiujinke"

    # websocket的请求地址
    MDM_URL = "http://mdm.kuainiu.io/"

    FILE_HOME = "/data1/"

    # celery 配置
    BROKER_URL = "redis://:kuainiujinke@redis-svc:6379/6"
    CELERY_RESULT_BACKEND = "redis://:kuainiujinke@redis-svc:6379/7"

    ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': 'redis://:kuainiujinke@redis-svc:6379/5',
            'default_timeout': 5
        }
    }

    # CELERY_REDIS_SCHEDULER_URL = 'redis://weidu@10.1.0.20:6379/8'

    # Jenkins run case 配置
    JENKINS_RUN_JOB = ["Auto_Test_Api_Run_Case11",
                       "Auto_Test_Api_Run_Case12",
                       "Auto_Test_Api_Run_Case13",
                       "Auto_Test_Api_Run_Case14",
                       "Auto_Test_Api_Run_Case15"]
