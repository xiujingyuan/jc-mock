# coding: utf-8
from sqlalchemy import Column, Integer, DateTime
from app import db
from app.common.Serializer import Serializer
from datetime import datetime


class TestTasksCase(db.Model, Serializer):
    __tablename__ = 'test_tasks_cases'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer)
    case_id = Column(Integer)
    task_version = Column(Integer, nullable=False)
    create_time = Column(DateTime, default=datetime.now)
