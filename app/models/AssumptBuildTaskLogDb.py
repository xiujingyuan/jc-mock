# coding: utf-8


from app.common.Serializer import Serializer
from app import db


class AssumptBuildTaskLog(db.Model, Serializer):
    __tablename__ = 'assumpt_build_task_log'

    id = db.Column(db.Integer, primary_key=True)
    build_task_id = db.Column(db.Integer)
    person = db.Column(db.String(11))
    modify_content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    modify_content_old = db.Column(db.Text)
