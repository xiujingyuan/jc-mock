# coding: utf-8
from sqlalchemy import BIGINT, Column, DateTime, String, text
from sqlalchemy.dialects.mysql.types import TINYINT
from app import db


class MobileDevice(db.Model):
    __tablename__ = 'mobile_device'
    __bind_key__ = "jihe"

    id = Column(BIGINT(), primary_key=True)
    imei = Column(String(64), unique=True)
    imei2 = Column(String(64), nullable=False, server_default=text("''"))
    mobile = Column(String(64), nullable=False, server_default=text("''"))
    mobile2 = Column(String(64), nullable=False, server_default=text("''"))
    version = Column(String(64), nullable=False, server_default=text("''"))
    is_root = Column(TINYINT(), nullable=False, server_default=text("'0'"))
    device = Column(String(64), nullable=False, server_default=text("''"))
    meid = Column(String(64), nullable=False, server_default=text("''"))
    create_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    last_heartbeat_at = Column(DateTime, nullable=False, server_default=text("'1000-01-01 00:00:00'"))
    heartbeat_at = Column(DateTime, nullable=False)
