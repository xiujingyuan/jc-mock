# coding: utf-8
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER
from app import db


class AssetQuality(db.Model):
    __tablename__ = 'asset_quality'
    __bind_key__ = "dh"

    asset_quality_id = Column(INTEGER(11), primary_key=True)
    item_sn = Column(INTEGER(11), nullable=False, comment='序号')
    statistical_date = Column(DateTime, comment='统计日期')
    asset_item_number = Column(String(64), nullable=False, unique=True, server_default=text("''"), comment='资产编号')
    product_cnt = Column(INTEGER(11), comment='产品期限')
    product_time_type = Column(String(64), comment='产品期限单位')
    item_cust_flg = Column(String(64), comment='用户类型信息')
    create_at = Column(DateTime)
    update_at = Column(DateTime)
    apply_user_type = Column(INTEGER(11), comment='子用户类型 0:未知 1:新客 2:老客 3:普通回流—新客 4:普通回流-老客 5:特殊回流—新客 6:特殊回流-老客 '
                                                  '7:次优新客 8:次优老客 9:次优回流—新客 10:次优回流-老客')
