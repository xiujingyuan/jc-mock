# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Text, String
from app import db
from app.common.Serializer import Serializer
from datetime import datetime


class TestTasksRun(db.Model, Serializer):
    __tablename__ = 'test_tasks_run'

    run_id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    run_task_id = Column(String(255, 'utf8_bin'))
    run_result = Column(Text(collation='utf8_bin'))
    run_begin = Column(DateTime, default=datetime.now)
    run_end = Column(DateTime)
    run_status = Column(Integer, default=1)
    run_jenkins_task_id = Column(Integer)
    run_env_num = Column(String(30, 'utf8_bin'))
    run_jenkins_job = Column(String(30, 'utf8_bin'))
