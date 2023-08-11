# coding: utf-8
from app import db


class CiLogInfo(db.Model):
    __tablename__ = 'ci_log_info'

    ci_log_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_log_pipeline_serial_num = db.Column(db.String(20), info='流水线id')
    ci_log_console_address = db.Column(db.String(1024), info='日志console地址')
    ci_log_build_number = db.Column(db.Integer)
    ci_log_console_info = db.Column(db.Text(collation='utf8_bin'), info='具体日志信息')
