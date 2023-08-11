#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/18
 @file: __init__.py.py
 @site:
 @email:
"""
from sqlalchemy import DateTime, Numeric, Date, Time, BLOB, LargeBinary
from datetime import datetime as cdatetime
from datetime import date, time


def convert_datetime(value):
    if value:
        if isinstance(value, (cdatetime, DateTime)):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, (date, Date)):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, (Time, time)):
            return value.strftime("%H:%M:%S")
    else:
        return ""


def model_to_dict(model):
    ret = {}
    for col in model.__table__.columns:
        value = getattr(model, col.name)
        if isinstance(col.type, DateTime):
            value = convert_datetime(value)
        elif isinstance(col.type, Numeric):
            value = float(value)
        elif isinstance(col.type, LargeBinary) and value is not None:
            value = str(value, encoding='utf-8')
        ret[col.name] = value
    return ret
