# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from app import db
from datetime import datetime
from app.common.Serializer import Serializer


class TestEnv(db.Model, Serializer):
    __tablename__ = 'test_env'

    id = Column(Integer, primary_key=True)
    env_id = Column(String(20, 'utf8_bin'))
    run_branch = Column(String(100, 'utf8_bin'))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    service_names = Column(String(255, 'utf8_bin'))
