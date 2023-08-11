# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from app import db


class Keyvalue(db.Model):
    __bind_key__ = "dh"
    __tablename__ = 'keyvalue'

    keyvalue_id = Column(INTEGER(11), primary_key=True)
    keyvalue_key = Column(String(100), nullable=False)
    keyvalue_value = Column(Text)
    keyvalue_memo = Column(Text)
    keyvalue_status = Column(Enum('active', 'inactive'), nullable=False, server_default=text("'active'"))
    keyvalue_create_user = Column(INTEGER(11), nullable=False)
    keyvalue_update_user = Column(INTEGER(11), nullable=False)
    keyvalue_create_at = Column(DateTime, nullable=False, server_default=text("'1000-01-01 00:00:00'"))
    keyvalue_update_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
