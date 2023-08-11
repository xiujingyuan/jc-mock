# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from app import db
from datetime import datetime
from app.common.Serializer import Serializer


class AssumptBuildTaskRun(db.Model, Serializer):
    __tablename__ = 'assumpt_build_task_run'

    id = Column(Integer, primary_key=True)
    build_task_run_id = Column(String(255), nullable=False)
    build_user = Column(String(30), nullable=False)
    build_time = Column(DateTime, default=datetime.now)
    build_branch = Column(String(11, 'utf8_bin'), nullable=False, server_default=FetchedValue())
    build_result = Column(Integer, nullable=False, server_default=FetchedValue())
    build_message = Column(Text(collation='utf8_bin'))
    build_task_id = Column(Integer, nullable=False)
    build_jenkins = Column(String(255), nullable=False)
    build_jenkins_task_id = Column(Integer, nullable=False)
    build_jenkins_queue_id = Column(Integer, nullable=False)
    build_env = Column(String(50), nullable=False)
    build_program_id = Column(Integer, nullable=False)
    build_commit_type = Column(Integer, default=1)
    build_param = Column(String(255), nullable=True)
    iteration_id = db.Column(db.String(100), nullable=False)
