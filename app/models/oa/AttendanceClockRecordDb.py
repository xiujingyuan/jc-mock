# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String, Time
from sqlalchemy.schema import FetchedValue
from app import db


class AttendanceClockRecord(db.Model):
    __tablename__ = 'attendance_clock_record'
    __bind_key__ = "oa"

    id = Column(Integer, primary_key=True)
    employee_no = Column(String(32), nullable=False, index=True)
    clock_date = Column(Date, nullable=False)
    clock_time = Column(Time, nullable=False)
    clock_desc = Column(String(255), nullable=False, server_default=FetchedValue())
    clock_place = Column(String(255), nullable=False, server_default=FetchedValue())
    clock_channel = Column(String(32), nullable=False, server_default=FetchedValue())
    is_across_work = Column(Integer, nullable=False, server_default=FetchedValue())
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=FetchedValue())
