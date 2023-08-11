# coding: utf-8
from sqlalchemy import Column, Date, DateTime, String
from sqlalchemy.schema import FetchedValue
from app import db


class SysUser(db.Model):
    __tablename__ = 'sys_user'
    __bind_key__ = "dh"

    id = Column(String(64), primary_key=True)
    company_id = Column(String(64), nullable=False, index=True)
    office_id = Column(String(64), nullable=False, index=True)
    login_name = Column(String(100), nullable=False, index=True)
    password = Column(String(100), nullable=False)
    no = Column(String(100))
    name = Column(String(100), nullable=False)
    email = Column(String(200))
    phone = Column(String(200))
    mobile = Column(String(200))
    user_type = Column(String(1))
    photo = Column(String(1000))
    login_ip = Column(String(100))
    login_date = Column(DateTime)
    login_flag = Column(String(64))
    create_by = Column(String(64), nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_by = Column(String(64), nullable=False)
    update_date = Column(DateTime, nullable=False, index=True)
    remarks = Column(String(255))
    del_flag = Column(String(1), nullable=False, index=True, server_default=FetchedValue())
    del_date = Column(Date)
