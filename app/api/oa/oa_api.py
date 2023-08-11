#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/04
 @file: oa_api.py
 @site:
 @email:
"""
import calendar
import random

from app import db, csrf
from app.api.oa import api_oa
from flask import jsonify, request

from app.models.oa.AttendanceClockRecordDb import AttendanceClockRecord


@api_oa.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Oa!'


@api_oa.route('/create_data', methods=['POST'])
@csrf.exempt
def create_data():
    ret = {
        "code": 0,
        "msg": "不是json格式请求"
    }
    request_data = request.json
    data_year = request_data["year"]
    data_month = request_data["month"]
    employee_no = request_data["employee_no"]
    name = request_data["name"]
    clock_type = request_data["clock_type"]
    last_day = calendar.monthrange(data_year, data_month)[1]
    try:
        for day in range(1, last_day+1):
            checkout_count = random.randint(0, 5)
            if checkout_count == 0:
                continue
            else:
                for checkout_index in range(1, checkout_count):
                    clock = AttendanceClockRecord()
                    clock.employee_no = employee_no
                    clock.clock_date = "{0}-{1}-{2}".format(data_year, data_month, day)
                    random_hour = random.randint(0, 23)
                    random_min = random.randint(0, 59)
                    random_sec = random.randint(0, 59)
                    clock.clock_time = "{0}:{1}:{2}".format(random_hour, random_min, random_sec)
                    clock.clock_desc = "考勤机：{0}".format(name) if clock_type == "machine" else "微信打卡：{0}".format(name)
                    clock.clock_channel = clock_type
                    clock.is_across_work = 0
                    clock.updated_at = "0000-00-00 00:00:00"
                    db.session.add(clock)
                db.session.flush()
    except Exception as e:
        ret["msg"] = e
    else:
        ret["code"] = 1
        ret["msg"] = "创建打卡记录成功"
    return jsonify(ret)



