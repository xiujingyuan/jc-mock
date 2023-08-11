# coding: utf-8
from app.common.Serializer import Serializer

from app import db


class SonarSchedule(db.Model, Serializer):
    __tablename__ = 'sonar_schedule'

    id = db.Column(db.Integer, primary_key=True, info='自增id')
    sonar_schedule_git_url = db.Column(db.String(50))
    sonar_schedule_project_key = db.Column(db.String(50))
    sonar_schedule_project_name = db.Column(db.String(50))
    sonar_schedule_branch = db.Column(db.String(50))
    sonar_schedule_status = db.Column(db.String(50))
    sonar_schedule_last_date = db.Column(db.DateTime)
    sonar_schedule_maven_version = db.Column(db.String(50))
    sonar_schedule_maven_extend = db.Column(db.String(200))
    sonar_sources = db.Column(db.String(50))
    sonar_exclusion = db.Column(db.String(50))
    sonar_language = db.Column(db.String(50))
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
