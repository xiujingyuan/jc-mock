# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER
from app import db


class GitlabProgram(db.Model):
    __tablename__ = 'gitlab_programs'

    id = Column(INTEGER(11), primary_key=True, comment='自增id')
    git_program_id = Column(INTEGER(11), nullable=False, comment='git上的项目的id')
    git_program_name = Column(String(255, 'utf8_bin'), nullable=False, server_default=text("''"), comment='git上的项目的名称')
    create_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
