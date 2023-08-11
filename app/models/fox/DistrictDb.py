# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import MEDIUMINT, SMALLINT, TINYINT
from app import db


class District(db.Model):
    __tablename__ = 'district'
    __bind_key__ = "dh"

    district_id = Column(SMALLINT(5), primary_key=True)
    district_code = Column(MEDIUMINT(8))
    district_name = Column(String(32), nullable=False)
    district_province_id = Column(SMALLINT(5))
    district_city_id = Column(SMALLINT(5))
    district_number = Column(String(5))
    district_level = Column(TINYINT(4), nullable=False, server_default=text("'2'"))
