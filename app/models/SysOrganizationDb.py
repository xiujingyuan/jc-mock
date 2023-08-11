# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from app import db
from app.common.Serializer import Serializer


class SysOrganization(db.Model, Serializer):
    __tablename__ = 'sys_organization'

    sys_organization_id = Column(Integer, primary_key=True)
    sys_organization_name = Column(String(30, 'utf8_bin'), nullable=False, server_default="")
    sys_organization_desc = Column(String(255, 'utf8_bin'))
    sys_organization_create_at = Column(DateTime, nullable=False, default=datetime.now)
    sys_organization_update_at = Column(DateTime, nullable=False, default=datetime.now)
    sys_organization_parent_id = Column(Integer)
    sys_organizations = db.relationship('SysProgram', backref='sys_organization', lazy='dynamic')
    sys_del_flag = Column(Integer,nullable=False, default=0)

    def __repr__(self):
        return self.sys_organization_name

    def serialize(self):
        return Serializer.serialize(self)
