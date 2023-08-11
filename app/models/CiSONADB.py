# coding: utf-8
from app import db




class CiSonaInfo(db.Model):
    __tablename__ = 'ci_sona_info'

    ci_sona_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_sona_pipeline_serial_num = db.Column(db.String(20), info='流水线id')
    ci_sona_ce_task_id = db.Column(db.String(20), info='ce任务taskid')
    ci_sona_bugs = db.Column(db.String(20), info='bug总数')
    ci_sona_vulnerabilities = db.Column(db.String(20), info='漏洞总数')
    ci_sona_debt = db.Column(db.String(20), info='debt总数')
    ci_sona_code_smells = db.Column(db.String(20), info='怀味道总数')
    ci_sona_coverage = db.Column(db.String(20), info='覆盖率')
    ci_sona_duplicateds = db.Column(db.String(20), info='重复度')
    ci_sona_duplicated_blocks = db.Column(db.String(20), info='重复块')
    ci_sona_create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')
    ci_sona_update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='更新时间')
