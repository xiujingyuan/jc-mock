# coding: utf-8

from sqlalchemy import Column
from app import db
from datetime import datetime


class ErrorLogs(db.Model):
    __tablename__ = 'error_logs'

    error_log_id = Column(db.INTEGER, primary_key=True)
    error_log_msg = Column(db.Text(collation='utf8_bin'))
    erro_log_create_at = Column(db.DateTime, default=datetime.now)
    error_log_update_at = Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
