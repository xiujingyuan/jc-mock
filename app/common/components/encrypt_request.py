#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/12/18
 @file: EncryptRequest.py
 @site:
 @email:
"""

import json
import hashlib
import hmac
import pyDes
import base64

des3key = "d3418y4KYhWM9pyotJQMV49L"

iv = des3key[0:8]

app_key = "1tbhIn5s014NEIatM8n44STe58XWOgjl"


def sign(sing_data):
    ret = hmac.new(bytes(app_key, encoding='utf-8'), bytes(sing_data, encoding='utf-8'),
                   digestmod=hashlib.sha256).digest().hex()
    return ret


def entry_data(data, mess):
    ret = {
        "data": encrypt_data(data).decode(),
        "mess": mess,
        # "timestamp": time.time(),
        "timestamp": 1544001888,
        "sign_type": "sha256"
     }
    sing_data = "data={0}&mess={1}&timestamp={2}&key={3}".format(ret["data"], ret["mess"], ret["timestamp"],
                                                                 app_key)
    ret["sign"] = sign(sing_data)
    return ret


def encrypt_data(data):
    print(type(data))
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, dict):
        data = json.dumps(data, ensure_ascii=False)
        data = data.encode("utf-8")
    elif not isinstance(data, bytes):
        raise TypeError("need bytes, but {0} type str".format(type(data)))
    data = data.replace(b" ", b"")
    k = pyDes.triple_des(des3key,  pyDes.CBC,  iv,  pad=None,  padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    print("Encrypted: %r" % d)
    print("Decrypted: %r" % k.decrypt(d))
    assert k.decrypt(d) == data
    ret_data = base64.b64encode(d)
    print(ret_data)
    return ret_data