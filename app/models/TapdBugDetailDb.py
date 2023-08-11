# coding: utf-8

from app.common.Serializer import Serializer
from app import db


class TapdBugDetail(db.Model, Serializer):
    __tablename__ = 'tapd_bug_detail'

    id = db.Column(db.Integer, primary_key=True)
    bug_id = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    bug_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    bug_workspace_id = db.Column(db.Integer, nullable=False)
    bug_iteration_id = db.Column(db.String(100, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    bug_story_id = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    program_id = db.Column(db.Integer, nullable=False)
    bug_create = db.Column(db.DateTime, nullable=False)
    bug_create_date = db.Column(db.Date, nullable=False)
    bug_status = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    bug_severity = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    find_version = db.Column(db.String(100, 'utf8_bin'), server_default=db.FetchedValue())
    bug_url = db.Column(db.String(255, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    is_effective = db.Column(db.Integer, server_default=db.FetchedValue())
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    bug_dev = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    bug_tester = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    bug_source = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    bug_reject_time = db.Column(db.DateTime, nullable=False)
    bug_reopen_time = db.Column(db.DateTime, nullable=False)

