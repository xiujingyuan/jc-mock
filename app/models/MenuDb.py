# coding: utf-8
from sqlalchemy import Column, Integer, LargeBinary, String
from app import db
from app.common.Serializer import Serializer


class Menu(db.Model, Serializer):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    parent = Column(Integer, index=True)
    route = Column(String(255))
    order = Column(Integer)
    data = Column(String(60))
    is_active = Column(Integer)

    def __repr__(self):
        return self.name

    def serialize(self):
        return Serializer.serialize(self)
