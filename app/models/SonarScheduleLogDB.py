# coding: utf-8
from app.common.Serializer import Serializer

from app import db


class SonarScheduleLog(db.Model, Serializer):
    __tablename__ = 'sonar_schedule_log'

    id = db.Column(db.Integer, primary_key=True, info='自增id')
    sonar_schedule_log_id = db.Column(db.Integer)
    sonar_schedule_log_project_key = db.Column(db.String(50))
    sonar_schedule_log_queue_id = db.Column(db.Integer)
    sonar_schedule_log_build_num = db.Column(db.String(50))
    sonar_schedule_log_console = db.Column(db.String(125))
    sonar_schedule_log_status = db.Column(db.String(50))
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
