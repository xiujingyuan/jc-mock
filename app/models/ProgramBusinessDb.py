# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db
from app.common.Serializer import Serializer


class ProgramBusiness(db.Model, Serializer):
    __tablename__ = 'program_business'

    business_id = Column(Integer, primary_key=True)
    program_id = Column(Integer, nullable=False, server_default=FetchedValue())
    business_name = Column(String(255), nullable=False, server_default=FetchedValue())
    create_at = Column(DateTime, server_default=FetchedValue())
    create_autor = Column(String(50), nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime, server_default=FetchedValue())
    business_cname = Column(String(200, 'utf8_bin'))
