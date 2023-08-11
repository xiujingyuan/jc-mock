# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


from app import db


class TapdTestPlanDetail(db.Model):
    __tablename__ = 'tapd_test_plan_detail'

    id = db.Column(db.Integer, primary_key=True)
    test_plan_id = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    test_plan_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    test_plan_workspace_id = db.Column(db.Integer, nullable=False)
    test_plan_iteration_id = db.Column(db.Integer, nullable=False)
    test_plan_story_id = db.Column(db.Integer, nullable=False)
    program_id = db.Column(db.Integer, nullable=False)
    test_plan_create = db.Column(db.DateTime, nullable=False)
    test_plan_create_date = db.Column(db.Date, nullable=False)
    test_plan_status = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    test_plan_url = db.Column(db.String(255, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
