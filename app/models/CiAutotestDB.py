# coding: utf-8
from app import db



class CiAutotestInfo(db.Model):
    __tablename__ = 'ci_autotest_info'

    ci_autotest_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_autotest_pipeline_serial_num = db.Column(db.String(20), info='流水线id')
    ci_autotest_total_num = db.Column(db.String(20), info='用例总数')
    ci_autotest_success_num = db.Column(db.String(20), info='用例成功数')
    ci_autotest_fail_num = db.Column(db.String(20), info='用例失败数')
    ci_autotest_success_rate = db.Column(db.String(20), info='用力成功率')
    ci_autotest_running_time = db.Column(db.String(50), info='用例执行时间')
    ci_autotest_report_address = db.Column(db.String(255), info='报告地址')
    ci_autotest_create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')
    ci_autotest_update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
