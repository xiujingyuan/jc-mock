# coding: utf-8
from app.common.Serializer import Serializer

from app import db


class CiPipeline(db.Model, Serializer):
    __tablename__ = 'ci_pipeline'

    ci_pipeline_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_pipeline_serial_num = db.Column(db.String(20), info='流水线序列号')
    ci_pipeline_trigger_type = db.Column(db.String(20), info='触发类型')
    ci_pipeline_trigger_user = db.Column(db.String(20), info='触发人')
    ci_pipeline_trigger_info = db.Column(db.Text(collation='utf8_bin'), info='触发信息')
    ci_pipeline_branch = db.Column(db.String(50), index=True, info='分支')
    ci_pipeline_source_branch = db.Column(db.String(50), index=True, info='分支')
    ci_pipeline_step = db.Column(db.String(20), info='当前步骤')
    ci_pipeline_address = db.Column(db.String(255), info='jenkins job地址')
    ci_pipeline_job_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='jenkins job表id')
    ci_pipeline_job_log_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='jenkins日志表id')
    ci_pipeline_autotest_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='自动化表id')
    ci_pipeline_sona_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='sona信息表id')
    ci_pipeline_build_num = db.Column(db.Integer, server_default=db.FetchedValue(), info='jenkins构建序号')
    ci_pipeline_env = db.Column(db.String(20), info='运行环境')
    ci_pipeline_status = db.Column(db.String(20), index=True, info='运行状态')
    ci_pipeline_run_time = db.Column(db.String(50), info='运行时间')
    ci_pipeline_handler_user = db.Column(db.String(255), info='处理人')
    ci_pipeline_handler_info = db.Column(db.String(255), info='处理信息')
    ci_pipeline_handler_times = db.Column(db.String(255), info='处理用时')
    ci_pipeline_create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')
    ci_pipeline_update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
