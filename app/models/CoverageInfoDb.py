# coding: utf-8
from app import db


class CoverageInfo(db.Model):
    __tablename__ = 'coverage_info'

    id = db.Column(db.Integer, primary_key=True)
    gitlab_program_id = db.Column(db.Integer)
    service_name = db.Column(db.String(50))
    branch = db.Column(db.String(255))
    compare_branch = db.Column(db.String(255))
    env = db.Column(db.String(20))
    content = db.Column(db.Text(collation='utf8_bin'))
    coverage_url = db.Column(db.String(255))
    line_coverage = db.Column(db.Float)
    version = db.Column(db.String(20, 'utf8_bin'))
    create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    new_coverage = db.Column(db.Integer)
