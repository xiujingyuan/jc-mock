# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class AppState(db.Model):
    __tablename__ = 'app_state'
    __bind_key__ = "jihe"

    id = Column(Integer, primary_key=True)
    employee_number = Column(String(64), nullable=False, index=True, server_default=FetchedValue())
    employee_name = Column(String(64), nullable=False, server_default=FetchedValue())
    employee_lead_number = Column(String(64), nullable=False, server_default=FetchedValue())
    employee_lead_name = Column(String(64), nullable=False, server_default=FetchedValue())
    mobile = Column(String(20), nullable=False, index=True, server_default=FetchedValue())
    device_area = Column(String(64), nullable=False, server_default=FetchedValue())
    device_id = Column(String(64), nullable=False, unique=True, server_default=FetchedValue())
    status = Column(Integer, nullable=False, server_default=FetchedValue())
    last_heartbeat_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    heartbeat_at = Column(DateTime, nullable=False)
    is_enable = Column(Integer, nullable=False, server_default=FetchedValue())
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    device_area_group_id = Column(String(64), nullable=False, server_default=FetchedValue())
    device_area_group_name = Column(String(255), nullable=False, server_default=FetchedValue())
