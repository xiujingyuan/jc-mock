# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text, BigInteger
from app import db
from app.common.Serializer import Serializer
from datetime import datetime


class TestTask(db.Model, Serializer):
    __tablename__ = 'test_tasks'

    task_id = Column(Integer, primary_key=True)
    task_title = Column(String(255, 'utf8_bin'))
    task_desc = Column(Text(collation='utf8_bin'))
    task_system = Column(Integer)
    task_business = Column(String(255, 'utf8_bin'))
    task_create_user = Column(String(25, 'utf8_bin'))
    task_last_user = Column(String(25, 'utf8_bin'))
    task_last_run_env = Column(String(30, 'utf8_bin'))
    task_create_time = Column(DateTime, default=datetime.now)
    task_update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    task_last_run_time = Column(DateTime)
    task_last_run_id = Column(String(50, 'utf8_bin'))
    task_version = Column(BigInteger, nullable=False)
    task_status = Column(Integer, default=0)
    task_last_result = Column(Integer)
    task_run_time = Column(Integer, default=0)
    task_type = Column(Integer, default=1)
