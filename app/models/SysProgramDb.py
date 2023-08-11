# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from app import db
from app.common.Serializer import Serializer


class SysProgram(db.Model, Serializer):
    __tablename__ = 'sys_program'

    sys_program_id = Column(Integer, primary_key=True)
    sys_program_name = Column(String(30, 'utf8_bin'), nullable=False, server_default="")
    sys_program_desc = Column(String(255, 'utf8_bin'))
    sys_program_group_id = Column(Integer, ForeignKey("sys_organization.sys_organization_id"))
    sys_program_create_at = Column(DateTime, nullable=False, default=datetime.now)
    sys_program_update_at = Column(DateTime, nullable=False, default=datetime.now)
    sys_sonar_key = Column(String(255))
    sys_sonar_type = Column(String(10), nullable=False, default="scan")
    tapd_work_ids = Column(String(255))
    git_program_ids = Column(String(255))
    sys_is_active = Column(Integer, nullable=False, default=1)

    def __repr__(self):
        return self.sys_program_name

    def serialize(self):
        return Serializer.serialize(self)
