# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text, MetaData
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.schema import FetchedValue
from app import db


class Keyvalue(db.Model):
    __tablename__ = 'keyvalue'
    __bind_key__ = "tmms"
    metadata = MetaData()

    keyvalue_id = Column(Integer, primary_key=True)
    keyvalue_key = Column(String(100), nullable=False)
    keyvalue_value = Column(Text)
    keyvalue_memo = Column(Text)
    keyvalue_status = Column(ENUM('active', 'inactive'), nullable=False, server_default=FetchedValue())
    keyvalue_create_user = Column(Integer, nullable=False)
    keyvalue_update_user = Column(Integer, nullable=False)
    keyvalue_create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    keyvalue_update_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    keyvalue_create_username = Column(String(256), server_default=FetchedValue())
    keyvalue_update_username = Column(String(256), server_default=FetchedValue())
