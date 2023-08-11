# coding: utf-8
from app import db


class ApiLog(db.Model):
    __tablename__ = 'api_log'

    api_log_id = db.Column(db.Integer, primary_key=True)
    api_log_url = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue(), info='访问的url')
    api_log_servername = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    api_log_method = db.Column(db.String(10), info='请求method')
    api_log_request_body = db.Column(db.Text, info='请求Body')
    api_log_response_body = db.Column(db.Text, info='返回结果')
    api_log_create_at = db.Column(db.DateTime, nullable=False, index=True, server_default=db.FetchedValue())
    api_log_update_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    api_log_user = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='api调用者')
    api_log_ip = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='请求的ip地址')
    api_log_is_success = db.Column(db.Integer, server_default=db.FetchedValue(), info='请求是否成功，0:失败，1:成功')
