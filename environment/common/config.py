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

import os
from base64 import b64decode
from datetime import datetime, timedelta

from celery.schedules import crontab
from kombu import Exchange, Queue

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    WTF_CSRF_SECRET_KEY = "my csrf key is easy"
    JWT_CSRF_SECRET_KEY = "my jwt key is not easy"
    SSL_DISABLE = False

    # CDN_HOST = "https://cdnjs.cloudflare.com/ajax/libs/"
    # CDN_HOST = "https://cdn.bootcss.com/"
    CDN_HOST = "https://cdn.bootcdn.net/ajax/libs/"

    # SQLALCHEMY设置配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_TIMEOUT = 10

    # 设置session和cookie过期时间
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    # REMEMBER_COOKIE_DURATION = timedelta(days=1)

    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "biz@kuainiu.io"
    MAIL_PASSWORD = "Q5F9ygX3ssNX9sSm"

    # email server
    # MAIL_SERVER = 'smtp.exmail.qq.com'
    # MAIL_RECEIVE_SERVER = 'imap.exmail.qq.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    # COM_MAIL_USERNAME = 'yangxuechao@kuainiugroup.com'
    # # COM_MAIL_PASSWORD = "Y22SBetb25YH353i"
    # COM_MAIL_PASSWORD = "E9i4s3onHaDuNV4j"

    JC_MOCK_MAIL_SUBJECT_PREFIX = '[Jc-Mock]'
    JC_MOCK_MAIL_SENDER = MAIL_USERNAME
    JC_MOCK_ADMIN = os.environ.get('Jc-Mock_ADMIN')
    JC_MOCK_POSTS_PER_PAGE = 20
    JC_MOCK_FOLLOWERS_PER_PAGE = 50
    JC_MOCK_COMMENTS_PER_PAGE = 30
    JC_MOCK_SLOW_DB_QUERY_TIME = 0.5
    # BACKEND_URL = "http://127.0.0.1:5002"
    BACKEND_URL = "http://testing-api.kuainiu.io"
    ENCRY_URL = 'http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/'
    # 国内资产同步测试环境，4套
    TEST1_ASSET_SYNC_URL = 'http://asset-sync1.test.k8s-ingress-nginx.kuainiujinke.com/asset/sync'
    TEST2_ASSET_SYNC_URL = 'http://asset-sync2.test.k8s-ingress-nginx.kuainiujinke.com/asset/sync'
    TEST3_ASSET_SYNC_URL = 'http://asset-sync3.test.k8s-ingress-nginx.kuainiujinke.com/asset/sync'
    TEST4_ASSET_SYNC_URL = 'http://asset-sync4.test.k8s-ingress-nginx.kuainiujinke.com/asset/sync'

    CN_ASSET_SYNC_URL = "http://asset-sync{0}.test.k8s-ingress-nginx.kuainiujinke.com/asset/sync"
    CN_RECOVERY_URL = "http://asset-sync{0}.test.k8s-ingress-nginx.kuainiujinke.com/asset/recovery"
    OVERSEA_ASSET_SYNC_URL = "http://fox-asset-sync-{0}.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset"
    OVERSEA_RECOVERY_URL = "http://fox-asset-sync-{0}.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/recovery"

    OVERSEA_ENCRY_URL = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/"
    # 海外资产同步测试环境，4个国家：泰国、菲律宾、墨西哥、巴基斯坦
    OVERSEA_TH_ASSET_SYNC_URL = 'http://fox-asset-sync-th.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset'
    OVERSEA_PH_ASSET_SYNC_URL = 'http://fox-asset-sync-ph.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset'
    OVERSEA_MX_ASSET_SYNC_URL = 'http://fox-asset-sync-mx.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset'
    OVERSEA_PK_ASSET_SYNC_URL = 'http://fox-asset-sync-pk.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset'
    OVERSEA_IN_ASSET_SYNC_URL = 'http://fox-asset-sync-ind.c99349d1eb3d045a4857270fb79311aa0.cn-shanghai.alicontainer.com/api/biz/sync/asset'

    IMAGE_URL = "/data/www/wwwroot/images"
    IMAGE_LINK_URL = "http://testing-images.kuainiu.io/"
    REDIRECT_URL = 'https://auto-vue.k8s-ingress-nginx.kuainiujinke.com/'

    # passport配置
    PASSPORT_CLIEND_ID = 18
    PASSPORT_CLIENT_SECRET = "AuSWC6sRk0ZgZeeqkzxNZsqtQZE9ZjGXRmpyXSBl"
    # PASSPORT_HEADER = "https://passport.qianxi.info"
    PASSPORT_HEADER = "https://oa.kuainiu.io/account"
    PASSPORT_CALLBACK_URL = "http://127.0.0.1:5102/auth/kuainiu/user/auth?authclient=kuainiu"
    PASSPORT_CODE_PATH = "/oauth/authorize?client_id={0}&redirect_uri={1}&response_type=code&scope=user.basic"
    PASSPORT_ACCESS_TOKEN_PATH = "/oauth/token"
    PASSPORT_USER_PATH = '/api/v1/users/me'

    PASSPORT_VUE_CLIEND_ID = 345
    PASSPORT_VUE_CLIENT_SECRET = "GEHSyXWST6HFl0cGL9DU7V43RrSK0gQ7FERoABjV"
    PASSPORT_VUE_CALLBACK_URL = "https://auto-vue.k8s-ingress-nginx.kuainiujinke.com/auth/callback"

    # websocket的请求地址
    MDM_URL = "http://mdm.kuainiu.io/"
    JC_REPORT_URL = "http://10.1.1.139:8088"
    test = datetime.now()
    JSON_AS_ASCII = False
    JAVASCRIPT = """(function(){
        var d=document,i=new Image,e=encodeURIComponent;
        i.src='%s/analytics/a.gif?url='+e(d.location.href)+'&ref='+e(d.referrer)+'&t='+e(d.title);
        })()""".replace('\n', '')
    BEACON = b64decode('R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==')

    log_base_dir = os.path.dirname(basedir)
    log_base_dir = os.path.dirname(log_base_dir)
    LOG_PATH = os.path.join(log_base_dir, 'logs')
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    # 轮转数量是 10 个
    LOG_FILE_BACKUP_COUNT = 10
    SENTRY_DSN = ""

    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6379"
    REDIS_PWD = "123456"
    # 上传文件地址
    UPLOAD_FOLDER = 'upload'
    DOWNLOAD_FOLDER = "download/excel"
    # rabbitmq
    RABBITMQ_HOST = "http://kong-api-test.kuainiujinke.com/qbus"
    RABBITMQ_URL = "/topic/messages/publish"
    RABBITMQ_USERNAME = "dh"
    RABBITMQ_PASSWORD = "7eb80d8eead3417d874f5571e289a017"

    CELERYBEAT_SCHEDULE = {
        'get_for_test_task': {
            'task': 'app.tasks.search_story.search_story_task.get_for_test',
            "schedule": timedelta(minutes=5),
            "args": ''
        },
        'get_diff_coverage_new_task': {
            'task': 'app.tasks.coverage_task.coverage_task.get_diff_coverage_new',
            "schedule": timedelta(minutes=5),
            "args": ''
        },
        'run_build_task': {
            'task': 'app.tasks.build_task.build_task.run_build_task',
            "schedule": timedelta(seconds=10),
            "args": ''
        },
        'get_run_auto_task': {
            'task': 'app.tasks.build_task.build_task.get_run_auto_task',
            "schedule": timedelta(seconds=20),
            "args": ''
        },
        'get_bug_map': {
            'task': 'app.tasks.test_report.report_task.get_bug_map',
            "schedule": crontab(hour="23,17"),
            "args": ''
        },
        'get_story_map': {
            'task': 'app.tasks.test_report.report_task.get_story_map',
            "schedule": crontab(hour="23,17"),
            "args": ''
        },
        'get_story_fields_info': {
            'task': 'app.tasks.test_report.report_task.get_story_fields_info',
            "schedule": crontab(hour="23,17"),
            "args": ''
        },
        'get_iteration_map': {
            'task': 'app.tasks.test_report.report_task.get_iteration_map',
            "schedule": crontab(hour="23,17"),
            "args": ''
        },
        'get_iteration_data': {
            'task': 'app.tasks.test_report.report_task.get_iteration_data',
            "schedule": crontab(hour="23,17"),
            "args": ''
        },

        'get_story_data': {
            'task': 'app.tasks.test_report.report_task.get_story_data',
            "schedule": crontab(hour="1,17", minute=0),
            "args": ''
        },
        'get_case_data': {
            'task': 'app.tasks.test_report.report_task.get_case_data',
            "schedule": crontab(hour="1,17", minute=30),
            "args": ''
        },
        'get_bug_data': {
            'task': 'app.tasks.test_report.report_task.get_bug_data',
            "schedule": crontab(hour="2,18", minute=0),
            "args": ''
        },
        'get_test_plan_data': {
            'task': 'app.tasks.test_report.report_task.get_test_plan_data',
            "schedule": crontab(hour="2,18", minute=30),
            "args": ''
        },
        # 'get_relation_data': {
        #     'task': 'app.tasks.test_report.report_task.get_relation_data',
        #     "schedule": crontab(hour=3),
        #     "args": ''
        # },

        'get_git_merge_data': {
            'task': 'app.tasks.test_report.report_task.get_git_merge_data',
            "schedule": crontab(hour="5,18", minute=0),
            "args": ''
        },
        'get_git_tag_data': {
            'task': 'app.tasks.test_report.report_task.get_git_tag_data',
            "schedule": crontab(hour="5,18", minute=20),
            "args": ''
        },
        'get_sonar_data': {
            'task': 'app.tasks.test_report.report_task.get_sonar_data',
            "schedule": crontab(hour="5,18", minute=40),
            "args": ''
        },

        'run_pipeline_task': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline',
            "schedule": timedelta(seconds=30),
            "args": ''
        },
        'run_pipeline_send_email': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_send_email',
            "schedule": timedelta(seconds=60),
            "args": ''
        },
        'sonar_schedule_create': {
            'task': 'app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_create',
            "schedule": timedelta(seconds=30),
            "args": ''
        },
        'sonar_schedule_query': {
            'task': 'app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_query',
            "schedule": timedelta(seconds=30),
            "args": ''
        },

        'run_pipeline_create_task_cmdb': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=1, minute=1),
            "args": ("master", '672')
        },
        'run_pipeline_create_task_contract': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=1, minute=31),
            "args": ("master", '1001')
        },
        'run_pipeline_create_task_grant': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=6, minute=1),
            "args": ("master", '335')
        },
        'run_pipeline_create_task_repay': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=8, minute=1),
            "args": ("master", '336')
        },
        'run_pipeline_create_task_global_grant': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=2, minute=1),
            "args": ("master", '1593')
        },
        'run_pipeline_create_task_global_repay': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=3, minute=1),
            "args": ("master", '1592')
        },
        'run_pipeline_create_task_global_payment': {
            'task': 'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task',
            "schedule": crontab(hour=4, minute=1),
            "args": ("master", '1589')
        }
    }
    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERYD_MAX_TASKS_PER_CHILD = 10
    CELERY_RESULT_EXPIRES = 3600
    CELERY_TASK_RESULT_EXPIRES = 300

    # CELERY_REDIS_MULTI_NODE_MODE = True
    # CELERY_REDIS_SCHEDULER_LOCK_TTL = 30
    # CELERY_BEAT_SCHEDULER = 'redisbeat.RedisScheduler'
    # CELERY_REDIS_SCHEDULER_KEY = 'celery:beat:order_tasks'

    # get_git_report_task
    CELERY_QUEUES = (
        Queue("app.tasks.search_story.search_story_task.get_for_test", Exchange("for_search_story_task"),
              routing_key="for_search_story_task"),
        Queue("app.tasks.common_task.calc_count.calc_count_task", Exchange("for_build_task"),
              routing_key="for_build_task"),
        Queue("app.tasks.build_task.build_task.run_build_task", Exchange("for_build_task"),
              routing_key="for_build_task"),
        Queue("app.tasks.build_task.build_task.get_run_auto_task", Exchange("for_build_task"),
              routing_key="for_build_task"),
        Queue("app.tasks.build_task.build_task.run_auto_task", Exchange("for_build_task"),
              routing_key="for_build_task"),
        Queue("app.tasks.build_task.build_task.get_git_report_task", Exchange("for_search_story_task"),
              routing_key="for_search_story_task"),
        Queue("app.tasks.case.case_task.run_case_by_case_id", Exchange("for_run_case_task"),
              routing_key="for_run_case_task"),
        Queue("app.tasks.coverage_task.coverage_task.get_diff_coverage_new", Exchange("for_search_story_task"),
              routing_key="for_search_story_task"),

        Queue("app.tasks.test_report.report_task.get_bug_map", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_story_map", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_story_fields_info", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_iteration_map", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_iteration_data", Exchange("for_report_task"),
              routing_key="for_report_task"),

        Queue("app.tasks.test_report.report_task.get_story_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_case_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_bug_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_test_plan_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        # Queue("app.tasks.test_report.report_task.get_relation_data", Exchange("for_report_task"),
        #       routing_key="for_report_task"),

        Queue("app.tasks.test_report.report_task.get_git_merge_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_git_tag_data", Exchange("for_report_task"),
              routing_key="for_report_task"),
        Queue("app.tasks.test_report.report_task.get_sonar_data", Exchange("for_report_task"),
              routing_key="for_report_task"),

        Queue("app.tasks.run_pipeline.run_pipeline_task.run_pipeline", Exchange("for_run_pipeline_task"),
              routing_key="for_run_pipeline_task"),
        Queue("app.tasks.run_pipeline.run_pipeline_task.run_pipeline_send_email", Exchange("for_run_pipeline_task"),
              routing_key="for_run_pipeline_task"),
        Queue("app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task", Exchange("for_run_pipeline_task"),
              routing_key="for_run_pipeline_task"),
        Queue("app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_create",
              Exchange("for_run_pipeline_task"),
              routing_key="for_run_pipeline_task"),
        Queue("app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_query",
              Exchange("for_run_pipeline_task"),
              routing_key="for_run_pipeline_task")
    )
    # celery路由
    CELERY_ROUTES = {
        'app.tasks.search_story.search_story_task.search_story_status': {
            "queue": "for_search_story_task",
            "routing_key": "for_search_story_task"
        },
        'app.tasks.search_story.search_story_task.get_for_test': {
            "queue": "for_search_story_task",
            "routing_key": "for_search_story_task"
        },
        'app.tasks.build_task.build_task.run_build_task': {
            "queue": "for_build_task",
            "routing_key": "for_build_task"
        },
        'app.tasks.build_task.build_task.get_run_auto_task': {
            "queue": "for_build_task",
            "routing_key": "for_build_task"
        },
        'app.tasks.build_task.build_task.run_auto_task': {
            "queue": "for_build_task",
            "routing_key": "for_build_task"
        },
        'app.tasks.common_task.calc_count.calc_count_task': {
            "queue": "for_build_task",
            "routing_key": "for_build_task"
        },
        'app.tasks.build_task.build_task.get_git_report_task': {
            "queue": "for_search_story_task",
            "routing_key": "for_search_story_task"
        },
        'app.tasks.case.case_task.run_case_by_case_id': {
            "queue": "for_run_case_task",
            "routing_key": "for_run_case_task"
        },
        'app.tasks.coverage_task.coverage_task.get_diff_coverage': {
            "queue": "for_search_story_task",
            "routing_key": "for_search_story_task"
        },
        'app.tasks.coverage_task.coverage_task.get_diff_coverage_new': {
            "queue": "for_search_story_task",
            "routing_key": "for_search_story_task"
        },

        'app.tasks.test_report.report_task.get_bug_map': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_story_map': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_story_fields_info': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_iteration_map': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_iteration_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },

        'app.tasks.test_report.report_task.get_story_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_case_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_bug_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_test_plan_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        # 'app.tasks.test_report.report_task.get_relation_data': {
        #     "queue": "for_report_task",
        #     "routing_key": "for_report_task"
        # },

        'app.tasks.test_report.report_task.get_git_merge_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_git_tag_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },
        'app.tasks.test_report.report_task.get_sonar_data': {
            "queue": "for_report_task",
            "routing_key": "for_report_task"
        },

        'app.tasks.run_pipeline.run_pipeline_task.run_pipeline': {
            "queue": "for_run_pipeline_task",
            "routing_key": "for_run_pipeline_task"
        },
        'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_send_email': {
            "queue": "for_run_pipeline_task",
            "routing_key": "for_run_pipeline_task"
        },
        'app.tasks.run_pipeline.run_pipeline_task.run_pipeline_create_task': {
            "queue": "for_run_pipeline_task",
            "routing_key": "for_run_pipeline_task"
        },
        'app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_create': {
            "queue": "for_run_pipeline_task",
            "routing_key": "for_run_pipeline_task"
        },
        'app.tasks.sonar_schedule.sonar_schedule_task.sonar_schedule_query': {
            "queue": "for_run_pipeline_task",
            "routing_key": "for_run_pipeline_task"
        }
    }

    # jenkins配置
    JENKINS_URL = "https://jenkins-test.kuainiujinke.com/jenkins/"
    USER_ID = "yangxuechao"
    USER_PWD = "11f3a93a50551a980fb261ee676c513137"

    JENKINS_DICT = {
        "https://jenkins-test.kuainiujinke.com/jenkins/": {
            "USER_ID": "yangxuechao",
            "USER_PWD": "11f3a93a50551a980fb261ee676c513137",
            "JACOCO_HOST": "http://10.1.1.139:8098",
            "JACOCO_FILE": "http://10.1.1.139:9089",
            "SUPER_JACOCO": ""
        },
        "https://jenkins.starklotus.com": {
            "USER_ID": "yangxuechao",
            "USER_PWD": "11f89fca9a7aa65d361b6bc7fa30888509",
            "JACOCO_HOST": "",
            "JACOCO_FILE": "",
            "SUPER_JACOCO": "https://super-jacoco.starklotus.com"
        },
        "https://k8s-test-jenkins.kuainiujinke.com/": {
            "USER_ID": "yangxuechao",
            "USER_PWD": "1134060894651292f2e74f334b272e17d4",
            "JACOCO_HOST": "",
            "JACOCO_FILE": "",
            "SUPER_JACOCO": "https://super-jacoco.k8s-ingress-nginx.kuainiujinke.com"
        },
    }

    COM_MAIL_USERNAME = 'testing-platform@qianshengqian.com'
    COM_MAIL_PASSWORD = "Kn201909"

    # administrator list
    ADMINS = ['yangxuechao@kuainiugroup.com']

    # 获取代码提交情况的接口地址
    GIT_MONTH_INFO = "/gitLog/getMothchStats"
    GIT_FILE_INFO = "/gitLog/getFileTypeCountByTime"
    GIT_TAG_INFO = "/gitLog/getTagInfo"

    # 获取覆盖率的地址
    # JACOCO_URL = "http://kong-api-test.kuainiujinke.com/jacoco-api/JacocoReportWS/
    # reportws/ReportServer/getJacocoReportAllByExculde"

    JACOCO_URL = "/JacocoReportWS/" \
                 "reportws/ReportServer/getJacocoReportAllByExculde"

    JACOCO_URL_BUILD = "/getJacocoReport/build"
    JACOCO_URL_UPDATE = "/asyncTask/update"
    JACOCO_URL_CLOSE = "/getJacocoReport/close"
    JACOCO_URL_MERGE = "/mergeReport/merge"
    SUPER_JACOCO_TRIGGER = "/cov/triggerEnvCov"
    SUPER_JACOCO_GET = "/cov/getEnvCoverResult"
    SUPER_JACOCO_STOP = "/cov/stopEnvCov"

    # 主题路径
    THEME_URL = "theme/"

    @staticmethod
    def init_app(app):
        pass
#         import logging
#         from logging.handlers import RotatingFileHandler
#         # Formatter
#         # formatter = logging.Formatter(
#         #     '%(asctime)s %(levelname)s %(process)d %(thread)d '
#         #     '%(pathname)s %(lineno)s %(message)s')
#         formatter = logging.Formatter("%(asctime)s %(levelname)s %(funcName)s: %(message)s")

#         # FileHandler Info
#         file_handler_info = RotatingFileHandler(filename=Config.LOG_PATH_INFO)
#         file_handler_info.setFormatter(formatter)
#         file_handler_info.setLevel(logging.INFO)
#         info_filter = logging.Filter()
#         info_filter.filter = lambda record: record.levelno >= logging.INFO
#         file_handler_info.addFilter(info_filter)
#         app.logger.addHandler(file_handler_info)

#         # FileHandler Error
#         file_handler_error = RotatingFileHandler(filename=Config.LOG_PATH_ERROR)
#         file_handler_error.setFormatter(formatter)
#         file_handler_error.setLevel(logging.ERROR)
#         error_filter = logging.Filter()
#         error_filter.filter = lambda record: record.levelno >= logging.ERROR
#         file_handler_error.addFilter(error_filter)
#         app.logger.addHandler(file_handler_error)


# class InfoFilter(logging.Filter):

#     def filter(self, record):
#         """only use INFO
#         筛选, 只需要 INFO 级别的log
#         :param record:
#         :return:
#         """
#         if logging.INFO <= record.levelno < logging.ERROR:
#             # 已经是INFO级别了
#             # 然后利用父类, 返回 1
#             return super().filter(record)
#         else:
#             return 0
