# coding: utf-8
from app import db
from app.common.Serializer import Serializer


class GitMergeInfo(db.Model, Serializer):
    __tablename__ = 'git_merge_info'

    id = db.Column(db.Integer, primary_key=True)
    merge_id = db.Column(db.Integer)
    merge_title = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    source_branch = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    target_branch = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    start_commit_sha = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    end_commit_sha = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    merge_create_user = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    merge_close_user = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    merge_create = db.Column(db.DateTime)
    merge_create_date = db.Column(db.Date)
    git_commit_count = db.Column(db.Integer)
    git_add_lines = db.Column(db.Integer)
    git_remove_lines = db.Column(db.Integer)
    git_changed_file = db.Column(db.Integer)
    gitlab_id = db.Column(db.Integer)
    gitlab_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    program_id = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def serialize(self):
        return Serializer.serialize(self)