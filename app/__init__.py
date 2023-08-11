#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/19
 @file: __init__.py.py
 @site:
 @email:
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.common.config.config import config
from flask_wtf.csrf import CSRFProtect
from redis import Redis
from celery import Celery
import os

# class MySQLAlchemy(SQLAlchemy):
#     def create_session(self, options):
#         options['autoflush'] = False
#         return SignallingSession(self, **options)


bootstrap = Bootstrap()
mail = Mail()
# db = MySQLAlchemy()
db = SQLAlchemy(session_options={"autocommit": True})
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

celery = Celery(__name__)


def create_app(config_name):
    app = Flask(__name__)
    # 导致指定的配置对象
    app.config.from_object(config[config_name])
    # 调用config.py的init_app()
    config[config_name].init_app(app)
    # app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    celery.conf.update(app.config)
    app.app_redis = Redis(host=app.config['REDIS_HOST'],
                          port=app.config['REDIS_PORT'],
                          db=5,
                          password=app.config['REDIS_PWD'])

    #
    # app.before_request(bind_request_params)
    # config[config_name].init_app(app)

    # 判断文件夹是否存在，如果不存在则创建
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(app.config["DOWNLOAD_FOLDER"]):
        os.makedirs(app.config["DOWNLOAD_FOLDER"])
    # csrf.init_app(app)
    # 初始化扩展
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app, )
    login_manager.init_app(app)

    from app.customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)

    from app.system import system as system_blueprint
    app.register_blueprint(system_blueprint, url_prefix="/system")

    from app.tool_set import tool_set as tool_set_blueprint
    app.register_blueprint(tool_set_blueprint, url_prefix="/tool/set")

    from app.setting import setting as setting_blueprint
    app.register_blueprint(setting_blueprint, url_prefix="/setting")

    from app.analytics import url_analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.assumpt_task import task_assumpt as task_assumpt_blueprint
    app.register_blueprint(task_assumpt_blueprint, url_prefix='/assumpt_task')

    from app.mock import mock_backend as mock_backend_blueprint
    app.register_blueprint(mock_backend_blueprint, url_prefix='/mock')

    from app.case import case as case_blueprint
    app.register_blueprint(case_blueprint, url='/case')

    from app.link import link as link_blueprint
    app.register_blueprint(link_blueprint, url='/link')

    from app.tasks import task_url as tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix="/tasks")

    from app.api.ci import ci_url as ci_blueprint
    app.register_blueprint(ci_blueprint, url='/ci')

    from app.api.test import test as api_test_blueprint
    app.register_blueprint(api_test_blueprint, url_prefix='/api/test')

    from app.api.nkz import nkz as api_nkz_blueprint
    app.register_blueprint(api_nkz_blueprint, url_prefix='/api/nkz')

    from app.api.tmms import tmms as api_tmms_blueprint
    app.register_blueprint(api_tmms_blueprint, url_prefix='/api/tmms')

    from app.api.jc_mock import mock as api_mock_blueprint
    app.register_blueprint(api_mock_blueprint, url_prefix="/api/mock")

    from app.api.case import api_case as api_case_blueprint
    app.register_blueprint(api_case_blueprint, url_prefix="/api/case")

    from app.api.oa import api_oa as api_oa_blueprint
    app.register_blueprint(api_oa_blueprint, url_prefix="/api/oa")

    from app.api.system import api_system as api_system_blueprint
    app.register_blueprint(api_system_blueprint, url_prefix="/api/system")

    from app.api.setting import api_setting as api_setting_blueprint
    app.register_blueprint(api_setting_blueprint, url_prefix="/api/setting")

    from app.api.report import api_report as api_report_blueprint
    app.register_blueprint(api_report_blueprint, url_prefix="/api/report")

    from app.api.dh import api_dh as api_dh_blueprint
    app.register_blueprint(api_dh_blueprint, url_prefix="/api/dh")

    from app.api.tools import api_tools as api_tools_blueprint
    app.register_blueprint(api_tools_blueprint, url_prefix="/api/tools")

    from app.api.contract import api_contract as api_contract_blueprint
    app.register_blueprint(api_contract_blueprint, url_prefix="/api/contract")

    from app.api.link import api_link as api_link_blueprint
    app.register_blueprint(api_link_blueprint, url_prefix="/api/link")

    from app.api.task import api_task as api_task_blueprint
    app.register_blueprint(api_task_blueprint, url_prefix="/api/task")

    from app.api.build_task import api_build_task as api_build_task_blueprint
    app.register_blueprint(api_build_task_blueprint, url_prefix="/api/build_task")

    from app.api.rabbitmq import api_rabbitmq as api_rabbitmq_blueprint
    app.register_blueprint(api_rabbitmq_blueprint, url_prefix="/api/rabbitmq")

    from app.api.coverage import api_coverage as api_coverage_blueprint
    app.register_blueprint(api_coverage_blueprint, url_prefix="/api/coverage")

    from app.api.tapd import api_tapd as api_tapd_blueprint
    app.register_blueprint(api_tapd_blueprint, url_prefix="/api/tapd")

    # report
    from app.report import view_report as view_report_blueprint
    app.register_blueprint(view_report_blueprint, url_prefix="/report/new")

    from app.api.statis_report import api_statistics_report as api_statistics_report_blueprint
    app.register_blueprint(api_statistics_report_blueprint, url_prefix="/api/statistics_report")

    from app.api.upload import view_upload as view_upload_blueprint
    app.register_blueprint(view_upload_blueprint, url_prefix="/api/upload")

    from app.api.download import api_download as api_download_blueprint
    app.register_blueprint(api_download_blueprint, url_prefix="/api/download")

    from app.api.quality_info import api_quality_info as api_quality_info_blueprint
    app.register_blueprint(api_quality_info_blueprint, url_prefix="/api/quality_info")

    from app.workspace import view_workspace as view_workspace_blueprint
    app.register_blueprint(view_workspace_blueprint, url_prefix="/workspace")

    from app.int import view_int as view_int_blueprint
    app.register_blueprint(view_int_blueprint, url_prefix="/int")

    return app


