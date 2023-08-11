# coding: utf-8
from app import db


class CiJobInfo(db.Model):
    __tablename__ = 'ci_job_info'

    ci_job_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_job_name = db.Column(db.String(50), info='jenkins job名')
    ci_job_type = db.Column(db.String(50), info='jenkins job类型')
    ci_job_deciption = db.Column(db.String(255), info='jenkins job描述')
    ci_job_address = db.Column(db.String(100), info='jenkins job地址')
    ci_job_sonar_address = db.Column(db.String(100), info='sonar 地址')
    ci_job_default_env = db.Column(db.String(50), info='jenkins job默认运行环境')
    ci_job_system = db.Column(db.String(50), info='jenkins job所属系统')
    ci_job_git_project_id = db.Column(db.Integer, info='jenkins job对应git项目id')
    ci_job_mail_receiver = db.Column(db.String(512), info='jenkins job所属系统')
