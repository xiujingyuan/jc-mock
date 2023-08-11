# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from app import db


class AssetSyncLog(db.Model):
    __tablename__ = 'asset_sync_log'
    __bind_key__ = "dh"

    id = Column(Integer, primary_key=True)
    asset_item_number = Column(String(64), nullable=False, index=True, server_default=FetchedValue())
    asset_type = Column(String(10), nullable=False)
    asset_sub_type = Column(String(10), nullable=False)
    asset_content = Column(Text, nullable=False)
    create_date = Column(Date, nullable=False, index=True)
    create_at = Column(DateTime, nullable=False, index=True)
    create_user_id = Column(Integer, nullable=False)
    create_user_name = Column(String(10), nullable=False, server_default=FetchedValue())
