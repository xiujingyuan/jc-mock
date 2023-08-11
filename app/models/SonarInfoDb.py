# coding: utf-8

from app.common.Serializer import Serializer
from app import db


class SonarInfo(db.Model, Serializer):
    __tablename__ = 'sonar_info'

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer)
    sonar_program_key = db.Column(db.String(20, 'utf8_bin'))
    sonar_program_name = db.Column(db.String(40, 'utf8_bin'))
    sonar_branch = db.Column(db.String(100, 'utf8_bin'))
    sonar_key = db.Column(db.String(40, 'utf8_bin'))
    sonar_bugs = db.Column(db.Integer)
    sonar_reliability_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_vulnerabilities = db.Column(db.Integer)
    sonar_security_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_sqale_index = db.Column(db.Integer)
    sonar_sqale_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_code_smells = db.Column(db.Integer)
    sonar_coverage = db.Column(db.Float)
    sonar_lines_to_cover = db.Column(db.Float)
    sonar_duplicated_blocks = db.Column(db.Integer)
    sonar_duplicated_lines = db.Column(db.Float)
    sonar_duplicated_lines_density = db.Column(db.Float)
    sonar_new_bugs = db.Column(db.Integer)
    sonar_new_reliability_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_new_vulnerabilities = db.Column(db.Integer)
    sonar_new_security_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_new_technical_debt = db.Column(db.Integer)
    sonar_new_maintainability_rating = db.Column(db.String(4, 'utf8_bin'))
    sonar_new_code_smells = db.Column(db.Integer)
    sonar_new_coverage = db.Column(db.Float)
    sonar_new_lines_to_cover = db.Column(db.Integer)
    sonar_new_duplicated_lines = db.Column(db.Float)
    sonar_new_duplicated_lines_density = db.Column(db.Float)
    sonar_new_lines = db.Column(db.Integer)
    sonar_branch_time = db.Column(db.DateTime, nullable=False)
    sonar_branch_year = db.Column(db.String(4, 'utf8_bin'), nullable=False)
    sonar_branch_month = db.Column(db.String(2, 'utf8_bin'), nullable=False)
    sonar_req = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    def serialize(self):
        return Serializer.serialize(self)