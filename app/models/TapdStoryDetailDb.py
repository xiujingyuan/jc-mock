# coding: utf-8
from app.common.Serializer import Serializer
from app import db


class TapdStoryDetail(db.Model, Serializer):
    __tablename__ = 'tapd_story_detail'

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    story_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    story_category = db.Column(db.String(25), nullable=False)
    story_tester = db.Column(db.String(25), nullable=False)
    story_developer = db.Column(db.String(25), nullable=False)
    story_workspace_id = db.Column(db.Integer, nullable=False)
    story_iteration_id = db.Column(db.String(100), nullable=False)
    story_create = db.Column(db.DateTime, nullable=False)
    story_create_date = db.Column(db.Date, nullable=False)
    story_completed = db.Column(db.DateTime, nullable=False)
    story_status = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    story_url = db.Column(db.String(255), nullable=False)
    is_effective = db.Column(db.Integer, server_default=db.FetchedValue())
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

