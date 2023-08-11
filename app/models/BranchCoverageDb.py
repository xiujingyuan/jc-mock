# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class BranchCoverage(Base):
    __tablename__ = 'branch_coverage'

    id = Column(Integer, primary_key=True)
    system = Column(String(60, 'utf8_bin'))
    branch = Column(String(255, 'utf8_bin'))
    tester = Column(String(60, 'utf8_bin'))
    coverage = Column(String(20, 'utf8_bin'))
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime, nullable=False, server_default=FetchedValue())
