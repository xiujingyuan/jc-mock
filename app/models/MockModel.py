# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import db


class Mock(db.Model):
    __tablename__ = 'mocks'

    mock_id = Column(Integer, primary_key=True)
    mock_name = Column(String(255, 'utf8_bin'))
    mock_desc = Column(String(255, 'utf8_bin'))
    mock_url = Column(String(255, 'utf8_bin'))
    mock_method = Column(String(255, 'utf8_bin'))
    mock_response = Column(Text(collation='utf8_bin'))
    mock_is_active = Column(Integer)
    mock_system = Column(Integer)
    mock_create_at = Column(DateTime)
    mock_update_at = Column(DateTime)

