# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class QualityInfo(db.Model):
    __tablename__ = 'quality_info'

    id = db.Column(db.Integer, primary_key=True, info='自增长，主键')
    task_id = db.Column(db.Integer, nullable=False, info='提测任务id')
    story_change_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='需求变更次数')
    smoke_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='冒烟次数')
    reason = db.Column(db.Text(collation='utf8_bin'), info='原因')
    quality_info_create_at = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    quality_info_update_at = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    operator = db.Column(db.String(20, 'utf8_bin'), nullable=False, server_default=db.FetchedValue(), info='操作人')
    level = db.Column(db.Integer, info='提测质量等级0:欠佳1:良好2:优')
