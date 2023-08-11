# coding: utf-8
from sqlalchemy import Column, String
from app import db


class AuthItemChild(db.Model):
    __tablename__ = 'auth_item_child'

    parent = Column(String(64, 'utf8_unicode_ci'), primary_key=True, nullable=False)
    child = Column(String(64, 'utf8_unicode_ci'), primary_key=True, nullable=False, index=True)
