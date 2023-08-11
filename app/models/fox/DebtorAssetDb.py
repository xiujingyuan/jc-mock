# coding: utf-8
from sqlalchemy import Column, DateTime, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from app import db


class DebtorAsset(db.Model):
    __tablename__ = 'debtor_asset'
    __bind_key__ = "dh"

    id = Column(INTEGER(11), primary_key=True)
    debtor_arrears_id = Column(INTEGER(11), nullable=False, index=True)
    debtor_id = Column(INTEGER(11), nullable=False, index=True)
    debtor_idnum = Column(String(64), nullable=False, index=True, server_default=text("''"))
    asset_id = Column(INTEGER(11), nullable=False, index=True)
    asset_item_number = Column(String(64), nullable=False, unique=True)
    create_at = Column(DateTime, nullable=False, server_default=text("'1000-01-01 00:00:00'"))
    create_user_id = Column(String(64), nullable=False)
    create_user_name = Column(String(100), nullable=False, server_default=text("''"))
    update_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    update_user_id = Column(String(64), nullable=False)
    update_user_name = Column(String(100), nullable=False, server_default=text("''"))
