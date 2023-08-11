# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy

from app.common.Serializer import Serializer

db = SQLAlchemy()


class GitCommitInfo(db.Model, Serializer):
    __tablename__ = 'git_commit_info'

    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    gitlab_id = db.Column(db.Integer, nullable=False)
    git_statics_date = db.Column(db.Date, nullable=False)
    git_commit_count = db.Column(db.Integer, nullable=False)
    iteration_id = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    git_add_lines = db.Column(db.Integer)
    git_remove_lines = db.Column(db.Integer, nullable=False)
    git_changed_file = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    is_effective = db.Column(db.Integer, server_default=db.FetchedValue())
    program_id = db.Column(db.Integer, nullable=False)
