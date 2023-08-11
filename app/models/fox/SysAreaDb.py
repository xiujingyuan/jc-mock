# coding: utf-8
from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.schema import FetchedValue
from app import db


class SysArea(db.Model):
    __tablename__ = 'sys_area'
    __bind_key__ = "dh"

    id = Column(String(64), primary_key=True)
    parent_id = Column(String(64), nullable=False, index=True)
    parent_ids = Column(String(2000), nullable=False)
    name = Column(String(100), nullable=False)
    sort = Column(Numeric(10, 0), nullable=False)
    code = Column(String(100))
    type = Column(String(1))
    create_by = Column(String(64), nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_by = Column(String(64), nullable=False)
    update_date = Column(DateTime, nullable=False)
    remarks = Column(String(255))
    del_flag = Column(String(1), nullable=False, index=True, server_default=FetchedValue())
