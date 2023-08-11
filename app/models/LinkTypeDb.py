# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from app import db


class LinkType(db.Model):
    __tablename__ = 'link_types'

    link_type_id = Column(Integer, primary_key=True)
    link_type_name = Column(String(255, 'utf8_bin'))
    link_type_create_at = Column(DateTime)

    mocks = Column(Integer)
    # mocks = db.relationship('Mock', backref='link_mock', lazy='dynamic')
