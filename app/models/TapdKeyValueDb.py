# coding: utf-8

from app import db


class TapdKeyValue(db.Model):
    __tablename__ = 'tapd_key_value'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    value = db.Column(db.Text, nullable=False)
    old_value = db.Column(db.Text, nullable=False)
    workspace_id = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
