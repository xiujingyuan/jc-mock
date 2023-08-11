#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/07
 @file: tmms_tools.py
 @site:
 @email:
"""
import asyncio
import datetime
import time
import traceback

import aiohttp
from flask import Flask, jsonify, request, current_app
import random
import json

from app import csrf
from app.api.tools import api_tools
from app.api.tools.tmms_models import UserInfo, ClsPushData
from app.common.random_infos import random_tele, random_name, gennerator


class ClsTmmsCase(object):
    def __init__(self):
        super(ClsTmmsCase, self).__init__()
        # self.loop = asyncio.get_event_loop()

    def create_push_data(self, from_system):
        userinfo = UserInfo()
        userinfo.phone = random_tele(is_false=False)
        userinfo.step = 0
        if isinstance(from_system, tuple):
            raise TypeError("need tuple type!")
        userinfo.from_system = random.choice(from_system)
        userinfo.valid_time = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        userinfo.click_time = time.strftime('%Y-%m-%d %H:%M:%S')
        userinfo.type = int(userinfo.from_system[-2:]) if userinfo.from_system != "DSQ" else random.randint(0, 2)
        clsdata = ClsPushData()
        clsdata.name = random_name()
        clsdata.identity = gennerator()
        clsdata.loan_limit = 0
        clsdata.finish_time = time.strftime('%Y-%m-%d %H:%M:%S')
        userinfo.data = clsdata
        return userinfo, None

    def send_datas(self, userinfos, url, headers=None):
        tasks = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if userinfos is not None:
            for userinfo in userinfos:
                coroutine = self.post_add_request(url, userinfo.change_json(), headers=headers)
                tasks.append(asyncio.ensure_future(coroutine))
            loop.run_until_complete(asyncio.wait(tasks))
            for task in tasks:
                current_app.logger.info(task.result())

    async def post_add_request(self, url, data, headers=None):
        if not isinstance(data, dict):
            raise TypeError("need dict type, but {0} found".format(type(data)))
        headers = {'content-type': 'application/json'} if headers is None else headers
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as resp:
                try:
                    return await resp.json()
                except:
                    return {"pot_error": traceback.format_exc()}


@api_tools.route('/dh/', methods=['POST'])
def test_dh():
    if "Content-Type" in request.headers and "application/json" in request.headers["Content-Type"]:
        args = request.json
        targetMobile = args["targetMobile"]
        content = args["content"]
        count = args["count"]
        current_app.create_task = True
        current_app.logger.info("begin".format(current_app.create_task))
        headers = {}
        # headers["X-Version"] = request.headers["X-Version"]
        # headers["X-Mobile"] = request.headers["X-Mobile"]
        # headers["X-Mobile2"] = request.headers["X-Mobile2"]
        # headers["X-Imei"] = request.headers["X-Imei"]
        # headers["X-Imei2"] = request.headers["X-Imei2"]
        # headers["X-Meid"] = request.headers["X-Meid"]
        # headers["X-IsRoot"] = request.headers["X-IsRoot"]
        # headers["X-WxXSpace"] = request.headers["X-WxXSpace"]
        # headers["X-Longitude"] = request.headers["X-Longitude"]
        # headers["X-Latitude"] = request.headers["X-Latitude"]
        # headers["X-Accuracy"] = request.headers["X-Accuracy"]
        # headers["X-RomVersion"] = request.headers["X-RomVersion"]
        mytmms = ClsTmmsCase()
        send_data = {
            "callRequestId": "0",
            "content": content,
            "currentMobile": "18140175758",
            "linkman": "null",
            "smsAt": time.time(),
            "smsId": random.randint(1000000000, 9000000000),
            "status": 32,
            "targetMobile": targetMobile,
            "type": 6,
            "baseObjId": 0
        }
        userinfos = []
        for _ in range(count):
            userinfos.append(send_data)
        mytmms.send_datas(userinfos, "http://kong-api-test.kuainiujinke.com/dh/audit-data-test1/sms-record",
                          headers=request.headers)

    return 'Hello Tools Tmms!'


@api_tools.route('/tmms/', methods=['GET'])
def hello_world():
    return 'Hello Tools Tmms!'


@api_tools.route('/tmms/create_task', methods=['POST', 'GET'])
def create_task():
    ret = {
        "code": 0,
        "msg": "不是json格式请求",
        "data": ""
    }
    if request.method == "POST":
        if "Content-Type" in request.headers and "application/json" in request.headers["Content-Type"]:
            args = request.json
            current_app.create_task = True
            current_app.logger.info("begin".format(current_app.create_task))
            num = args["num"]
            customer_channel = args["customer_channel"]
            customer_os = args["customer_os"]
            customer_app = args["customer_app"]
            from_system = args["from_system"]
            create_round = args["create_round"]
            mytmms = ClsTmmsCase()
            icount = 0
            max_num = num / create_round
            min_num = create_round if num > create_round else num
            while True:
                if icount >= max_num:
                    break
                userinfos = []
                while True:
                    userinfo, _ = mytmms.create_push_data(from_system)
                    userinfo.customer_channel = random.choice(customer_channel)
                    userinfo.customer_os = random.choice(customer_os)
                    userinfo.customer_app = random.choice(customer_app)
                    if len(userinfos) == min_num:
                        break
                    userinfos.append(userinfo)
                icount += 1
                mytmms.send_datas(userinfos, "http://tmms-testing.kuainiujinke.com/v1/cust-info/push")
                time.sleep(1)
                ret["code"] = 1
                ret["msg"] = "发送成功!"
            current_app.create_task = False

            current_app.logger.info("end {0}".format(current_app.create_task))
    elif request.method == "GET":
        ret["code"] = 1
        ret["msg"] = "获取成功!"
        ret["data"] = current_app.create_task if hasattr(current_app, "create_task") else False
    print(ret)
    return jsonify(ret)
