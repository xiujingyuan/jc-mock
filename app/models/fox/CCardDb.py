# coding: utf-8
from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from app import db


class CCard(db.Model):
    __tablename__ = 'c_card'
    __bind_key__ = "dh"

    id = Column(INTEGER(11), primary_key=True)
    asset_item_number = Column(String(64), nullable=False, unique=True, server_default=text("''"))
    customer_type = Column(String(10))
    d3_score = Column(String(20))
    d3_level = Column(INTEGER(20))
    d7_score = Column(String(20))
    d7_level = Column(String(20))
    m1_score = Column(String(20))
    m1_level = Column(String(20))
    special_risk = Column(String(10))
    create_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    m1plus_score = Column(String(64))
    m1plus_level = Column(String(20))
    self_healing = Column(String(5), server_default=text("'0'"), comment='自愈案件标志 0 不是,1 是')
