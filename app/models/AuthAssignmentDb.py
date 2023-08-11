# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, SmallInteger, String, Text
from sqlalchemy.orm import relationship
from app import db


class AuthAssignment(db.Model):
    __tablename__ = 'auth_assignment'

    item_name = Column(ForeignKey('auth_item.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    user_id = Column(String(64, 'utf8_unicode_ci'), primary_key=True, nullable=False, index=True)
    created_at = Column(Integer)

    auth_item = relationship('AuthItem', primaryjoin='AuthAssignment.item_name == AuthItem.name', backref='auth_assignments')


class AuthItem(db.Model):
    __tablename__ = 'auth_item'

    name = Column(String(64, 'utf8_unicode_ci'), primary_key=True)
    type = Column(SmallInteger, nullable=False, index=True)
    description = Column(Text(collation='utf8_unicode_ci'))
    rule_name = Column(ForeignKey('auth_rule.name', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    data = Column(LargeBinary)
    created_at = Column(Integer)
    updated_at = Column(Integer)

    auth_rule = relationship('AuthRule', primaryjoin='AuthItem.rule_name == AuthRule.name', backref='auth_items')


class AuthRule(db.Model):
    __tablename__ = 'auth_rule'

    name = Column(String(64, 'utf8_unicode_ci'), primary_key=True)
    data = Column(LargeBinary)
    created_at = Column(Integer)
    updated_at = Column(Integer)
