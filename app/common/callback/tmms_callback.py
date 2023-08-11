#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/12/20
 @file: send_callback.py
 @site:
 @email:
"""
from copy import deepcopy
import random

from app.common.send_request.send_data import send_data

url_detail = "http://tmms-testing.kuainiujinke.com/emic-ivr/callRecordDetail"

url_complete = "http://tmms-testing.kuainiujinke.com/emic-ivr/taskComplete"

url_callback_establish = "http://tmms-testing.kuainiujinke.com/emic/call-establish"
url_callback_hang_up = "http://tmms-testing.kuainiujinke.com/emic/call-hang-up"


def random_detail(phone):
    call_result = random.randint(0, 6)
    manual_status = random.randint(0, 3) if call_result == 2 else 0
    # call_result = 2
    # manual_status = 1
    ret = {
            "count": 1,
            "uuid": "kuainiu1218",
            "records": [{
                "task_id": 6901,
                "script_name": "修改话术名称",
                "callee_phone": phone,
                "cc_number": "20017_00000010conf0_{0}".format(phone),
                "calllog_txt": "<calllog>\n    <item action=\"dialog\" timeseconds=\"1545632113\" user=\"ai\" ai_"
                               "voice_type=\"\">您好！我是贷上钱服务中心，给您来电话是看到您近期注册申请贷上钱借款时额度没有申请成"
                               "功，您现在还是需要通过我们平台借款的对吗？<\/item>\n    <item action=\"dialog\" timeseconds"
                               "=\"1545632129\" user=\"clue\" keywords=\"\">哦没有<\/item>\n    <item action=\"match\""
                               " timeseconds=\"1545632129\" score=\"1\" match_cluster_name=\"开场白否定\/拒绝\" match_"
                               "standard_question=\"\">没有<\/item>\n    <item action=\"dialog\" timeseconds=\"1545632"
                               "129\" user=\"ai\" ai_voice_type=\"\">那您可以先了解一下，我们公司”贷上钱“是一家信用借款平台"
                               "，无担保无抵押、不查征信，额度评估最快只需要2分钟，您有兴趣了解一下吗？<\/item>\n    <item ac"
                               "tion=\"dialog\" timeseconds=\"1545632142\" user=\"clue\" keywords=\"\">三三件<\/item"
                               ">\n    <item action=\"match\" timeseconds=\"1545632142\" score=\"0\" match_cluster_na"
                               "me=\"\" match_standard_question=\"\"><\/item>\n    <item action=\"dialog\" timeseco"
                               "nds=\"1545632142\" user=\"ai\" ai_voice_type=\"nomatch\">那这样，我马上帮您转接客户经理给"
                               "您做详细的介绍，请问您贵姓啊？<\/item>\n    <item action=\"dialog\" timeseconds=\"15456"
                               "32151\" user=\"clue\" keywords=\"\">不用<\/item>\n    <item action=\"match\" timesec"
                               "onds=\"1545632151\" score=\"1\" match_cluster_name=\"邀约否定\/拒绝\" match_standard_"
                               "question=\"\">不用<\/item>\n    <item action=\"dialog\" timeseconds=\"1545632151\" u"
                               "ser=\"ai\" ai_voice_type=\"\">不好意思打扰您了，祝您生活愉快，再见。<\/item>\n<\/calllog>\n",
                "call_result": call_result,
                "call_time": 1545632101,
                "duration": random.randint(1, 200),
                "intention_type": 1,
                "manual_status": manual_status,
                "label": "",
                "call_count": 1,
                "record_url": "",
                "answer_time": 0,
                "hangup_time": 0,
                "match_global_keyword": "{}"
            }]
        }

    if call_result == 2 and manual_status == 2:
        ret["records"][0]["transfer_number"] = "{0}_000136e5".format(random.choice((1006, 1007, 1008)))
        # ret["records"][0]["transfer_number"] = "sdfas_sdfdsf"
        ret["records"][0]["transfer_duration"] = random.randint(1, 100)

    return ret


def call_record_detail_callback():
    """
    通话记录回调接口
    :返回格式，非0：失败
    {
        "retcode" : 0,
        "reason" : "请求成功"
    }
    """
    data_list = []
    data = {
        "count": 1000,
        "uuids": "121212",
        "records": []
    }

    phones = []
    import os
    base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "phone.txt")
    print(file_path)
    with open(file_path) as read_phone:
        for phone in read_phone.readlines():
            # if len(phones) > 99:
            #     break
            phones.append(phone.strip("\n"))
    # print(phones)

    # phones = ["13980522295",
    #           "18683890068"]
    # phones = ["18220413576"]
    for phone in phones:
        # data_phone = deepcopy(data)
        # data_phone["records"].append(random_detail(phone))
        data_list.append(random_detail(phone))

    send_data(url_detail, data_list)


def task_complete_callback():
    """
    任务完成详情回调接口
    :返回格式，非0：失败
    {
        "retcode" : 0,
        "reason" : "请求成功"
    }
    """
    data_list = []
    data = {
        "uuid": 121212,
        "task_id": 579,
        "task_name": "v4_test-100-sf",
        "statistics": {
            "intention_a": 1,
            "intention_b": 1,
            "intention_c": 1,
            "intention_d": 1,
            "intention_e": 1,
            "called": 1,
            "call_failed": 2,
            "call_success": 2,
            "call_answer_no": 2,
            "call_answer_hangup": 2,
            "duration_5_10": 2,
            "duration_10_30": 2,
            "duration_30_60": 2,
            "duration_60_120": 2,
            "duration_120": 2
        }
    }
    data_list.append(data)
    send_data(url_complete, data_list)


def call_establish():
    """
    回调建立连接
    :return:
    """
    data_list = []
    data = {
        "callId": "api010000134161548233555665MB5G4",
        "accountSid": "304d4bd24c943b380c07791ff02b0cd1",
        "appId": "adae52e0c4a587c0ac8a2fa16ee6d53d",
        "caller": "073188194073",
        "called": "13980522295",
        "startTime": "20190123141331",
        "type": "2",
        "ringDuration": "21",
        "callType": "0"
    }
    data_list.append(data)
    send_data(url_callback_establish, data_list)


def call_hang_up():
    """
    回调挂断连接
    :return:
    """
    data_list = []
    data = {
          "callId": "api010000134161548233555665MB5G4",
          "accountSid": "304d4bd24c943b380c07791ff02b0cd1",
          "appId": "adae52e0c4a587c0ac8a2fa16ee6d53d",
          "caller": "073188194076",
          "called": "13980522295",
          "startTime": "20190123142945",
          "stopTime": "20190123143059",
          "duration": "74",
          "reason": "1001",
          "state": "0",
          "type": "3",
          "callType": "0",
          "ringDuration": "18"
        }
    data_list.append(data)
    send_data(url_callback_hang_up, data_list)


if __name__ == "__main__":
    # task_complete_callback()
    # call_record_detail_callback()
    # call_establish()
    call_hang_up()
