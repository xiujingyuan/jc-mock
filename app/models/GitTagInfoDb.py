# coding: utf-8

from flask_sqlalchemy import SQLAlchemy
from app import db


class GitTagInfo(db.Model):
    __tablename__ = 'git_tag_info'

    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    tag_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    tag_gitlab_id = db.Column(db.Integer, nullable=False)
    tag_create = db.Column(db.DateTime, nullable=False)
    tag_create_date = db.Column(db.Date, nullable=False)
    tag_message = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    tag_commit_id = db.Column(db.String(255, 'utf8_bin'))
    tag_commit_message = db.Column(db.String(255, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    is_effective = db.Column(db.Integer, server_default=db.FetchedValue())
    program_id = db.Column(db.Integer, nullable=False)
