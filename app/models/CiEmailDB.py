# coding: utf-8
from app import db


class CiEmail(db.Model):
    __tablename__ = 'ci_email'

    ci_email_id = db.Column(db.Integer, primary_key=True, info='自增id')
    ci_email_serial_num = db.Column(db.String(50), info='邮件流水号')
    ci_email_recipients = db.Column(db.String(255), info='邮件收件人')
    ci_email_subject = db.Column(db.String(100), info='邮件主题')
    ci_email_status = db.Column(db.String(50), info='邮件状态')
    ci_email_html = db.Column(db.Text(collation='utf8_bin'), info='邮件内容')
    ci_email_create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='创建时间')

