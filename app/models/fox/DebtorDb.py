# coding: utf-8
from sqlalchemy import Column, DateTime, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT
from app import db


class Debtor(db.Model):
    __tablename__ = 'debtor'
    __bind_key__ = "dh"
    __table_args__ = (
        Index('uk_idnum_customer_id', 'idnum', 'original_customer_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    original_customer_id = Column(String(64), nullable=False, server_default=text("''"))
    name = Column(String(255), nullable=False, index=True, server_default=text("''"))
    idnum = Column(String(64), nullable=False, server_default=text("''"))
    nation = Column(String(16), server_default=text("''"))
    tel = Column(String(20), nullable=False, index=True, server_default=text("''"))
    gender = Column(String(2), nullable=False, server_default=text("''"))
    status = Column(String(16), nullable=False, server_default=text("''"))
    province = Column(String(32), nullable=False, server_default=text("''"))
    province_code = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    city = Column(String(32), nullable=False, server_default=text("''"))
    city_code = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    permanent = Column(String(128), nullable=False)
    residence = Column(String(128), nullable=False, server_default=text("''"))
    workplace = Column(String(128), nullable=False, server_default=text("''"))
    company = Column(String(255), nullable=False, server_default=text("''"))
    work_tel = Column(String(20), nullable=False, server_default=text("''"))
    residence_tel = Column(String(20), nullable=False, server_default=text("''"))
    create_at = Column(DateTime, nullable=False, server_default=text("'1000-01-01 00:00:00'"))
    create_user_id = Column(String(64), nullable=False)
    create_user_name = Column(String(100), nullable=False, server_default=text("''"))
    update_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    update_user_id = Column(String(64), nullable=False)
    update_user_name = Column(String(100), nullable=False, server_default=text("''"))
