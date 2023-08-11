#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/20
 @file: send_data.py
 @site:
 @email:
"""
import time
import aiohttp
import asyncio
import json


now = lambda: time.time()


async def post_add_request(url, data, headers=None):
    start = now()
    if headers is not None:
        headers = headers
    else:
        headers = {}
        headers['content-type'] = 'application/json'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as resp:
            print("post_add_requst time:", now() - start)
            return await resp.text()


def send_data(url, data_list, headers=None):
    for data in data_list:
        print(json.dumps(data, ensure_ascii=False))
    if headers is None:
        cor_list = list(map(lambda x: post_add_request(url, x, headers=headers), data_list))
    else:
        cor_list = list(map(lambda x, y: post_add_request(url, x, headers=y), data_list, headers))
    loop = asyncio.get_event_loop()
    start = now()
    tasks = list(map(lambda x: asyncio.ensure_future(x), cor_list))
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        try:
            print(task.result().encode('latin-1').decode('unicode_escape'))
        except:
            print('Task ret: ', task.result())
    print("TIME:", now() - start)
