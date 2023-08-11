# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text
from app import db
from datetime import datetime
from app.common.Serializer import Serializer


class JenkinsJob(db.Model, Serializer):
    __tablename__ = 'jenkins_jobs'

    jenkins_id = Column(Integer, primary_key=True)
    jenkins_job_name = Column(String(100, 'utf8_bin'))
    jenkins_url = Column(String(200, 'utf8_bin'))
    jenkinis_params = Column(Text(collation='utf8_bin'))
    jenkinis_create_at = Column(DateTime, default=datetime.now)
    jenkinis_update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    gitlab_program_id = Column(Integer, default=0)
    gitlab_program_http_url = Column(String(100, 'utf8_bin'))
    service_name = Column(String(255, 'utf8_bin'))
    git_module = Column(Text(collation='utf8_bin'))
    is_active = Column(Integer, default=0)
    change_ip = Column(Integer, default=1)
    is_collect = Column(Integer, default=0)
    mvn_version = Column(Integer, default=0)
    mvn_extend = Column(String(255, 'utf8_bin'))
