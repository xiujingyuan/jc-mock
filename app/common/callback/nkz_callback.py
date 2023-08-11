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
from functools import reduce

from app.common.entry_data.nkz.data_encrypt import entry_data
from app.common.send_request.send_data import send_data

url = "http://nkz-api-testing.kuainiujinke.com/pay/callback?channel=YUN"


def yun_pay_callback():
    data_list = []
    data = {
            "code": "0000",
            "data": {
                "order_id": "YUN2018121411214899975154",
                "pay": "9.94",
                "broker_id": "27532644",
                "dealer_id": "23665418",
                "real_name": "六九",
                "card_no": "6217000830000123038",
                "id_card": "346136199406139437",
                "status": "2",
                "status_detail": "1000",
                "status_message": "待打款",
                "sys_amount": "0.00",
                "broker_amount": "0.00",
                "tax": "0.00",
                "ref": "17457240105107497328",
                "withdraw_platform": "bankpay",
                "created_at": "2018-12-06 20:37:54",
                "finished_time": "2018-12-06 20:37:54",
                "sys_fee": "0.00",
                "broker_fee": "0.00"
            },
            "message": "操作成功",
            "request_id": "5c09186b08d28"
        }
    ret = entry_data(data, "5c0799605584e")
    data_list.append(ret)
    send_data(url, data_list)


url_bone = "http://nkz-api-testing.kuainiujinke.com/pb/bonus/cash"
url_bone_real = "https://nkz-api.kuainiujinke.com/pb/bonus/cash"


def get_bone():
    data_list = []
    data = {
            "cashKey": "type_business_cash"
        }
    token_list = ["token_aaaaa", "token_abcdef",
                  "d7ce425c36c20c33fe6c3edcf9cbfdd9c3ea6601251d7046a68b7218c5ba0ca8"]


    # for _ in range(10):
    #     datas.append(data)

    headers_list = []
    for index in range(1):
        data_list.append(data)
        headers = {}
        headers['content-type'] = 'application/json'
        headers["deviceType"] = "app_android"
        headers["token"] = token_list[index]
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                "Chrome / 67.0.3396.99Safari / 537.36"

        headers_list.append(headers)

    send_data(url_bone, data_list, headers=headers_list)


if __name__ == "__main__":
    # yun_pay_callback()
    get_bone()

