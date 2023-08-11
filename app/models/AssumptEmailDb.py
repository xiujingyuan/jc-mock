# coding: utf-8
from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from app import db
from app.common.Serializer import Serializer


class AssumptEmail(db.Model, Serializer):
    __tablename__ = 'assumpt_email'

    id = Column(INTEGER(11), primary_key=True, comment='自增id')
    email_id = Column(INTEGER(11), nullable=False, comment='邮件ID')
    email_from = Column(VARCHAR(255), nullable=False, server_default=text("''"), comment='发送方')
    email_to = Column(Text, nullable=False, server_default=text("''"), comment='接收方')
    email_content = Column(TEXT, nullable=False, comment='内容')
    email_attach = Column(VARCHAR(11), comment='附件')
    mail_receive_time = Column(DateTime, nullable=False, comment='邮件接收时间')
    create_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='记录创建时间')
    story_id = Column(VARCHAR(255), comment='关联需求id')
    story_full_id = Column(VARCHAR(255), comment='关联需求的完整版id')
    work_id = Column(VARCHAR(20), comment='关联需求所在的项目id(tapd)')
    href_value = Column(Text(collation='utf8_bin'), comment='包含的链接')
    subject = Column(String(255, 'utf8_bin'), comment='标题')
