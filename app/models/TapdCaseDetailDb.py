# coding: utf-8

from app import db


class TapdCaseDetail(db.Model):
    __tablename__ = 'tapd_case_detail'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    case_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    case_workspace_id = db.Column(db.Integer, nullable=False)
    case_iteration_id = db.Column(db.Integer, nullable=False)
    case_story_id = db.Column(db.Integer, nullable=False)
    program_id = db.Column(db.Integer, nullable=False)
    case_create = db.Column(db.DateTime, nullable=False)
    case_create_date = db.Column(db.Date, nullable=False)
    case_precondition = db.Column(db.Text(collation='utf8_bin'))
    case_steps = db.Column(db.Text(collation='utf8_bin'))
    case_expectation = db.Column(db.Text(collation='utf8_bin'))
    case_status = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    case_priority = db.Column(db.String(25, 'utf8_bin'))
    case_type = db.Column(db.String(25, 'utf8_bin'))
    case_url = db.Column(db.String(255, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    case_category_id = db.Column(db.String(100, 'utf8_bin'), nullable=False, server_default=db.FetchedValue())
    case_creator = db.Column(db.String(20, 'utf8_bin'))
    is_pass = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

