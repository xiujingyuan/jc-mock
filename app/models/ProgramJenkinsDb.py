# coding: utf-8
from sqlalchemy import Column, DateTime, Integer
from app import db
from datetime import datetime
from app.common.Serializer import Serializer


class ProgramJenkin(db.Model, Serializer):
    __tablename__ = 'program_jenkins'

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer)
    jenkins_id = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
