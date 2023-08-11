# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app import db


class UserLink(db.Model):
    __tablename__ = 'user_link'

    user_link_id = Column(Integer, primary_key=True)
    user_link_link_id = Column(ForeignKey('links.link_id'), index=True)
    user_link_user_id = Column(ForeignKey('users.id'), index=True)
    user_link_link_count = Column(Integer, default=0)
    user_link_create_at = Column(DateTime, nullable=False, default=datetime.now)
    user_link_update_at = Column(DateTime, nullable=False, default=datetime.now)

    user_link_link = relationship('Link', primaryjoin='UserLink.user_link_link_id == Link.link_id', backref='user_links')
    user_link_user = relationship('User', primaryjoin='UserLink.user_link_user_id == User.id', backref='user_links')
