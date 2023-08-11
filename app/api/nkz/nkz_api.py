from flask import Flask, jsonify, request

from app.common.components.encrypt_request import entry_data

from app.api.nkz import nkz


@nkz.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@nkz.route('/certification/verify-id-card', methods=['POST', 'GET'])
def verify_id_card():
    """
    身份证实名验证接口
    :return:
    """
    data = {"id_card": None, "real_name": None}
    ret = entry_data(data, "5c0799605584e")
    print(ret)
    return jsonify(ret)


@nkz.route('/authentication/verify-bankcard-three-factor', methods=['POST'])
def verify_bankcard_three_factors():
    """
    银行卡三要素接口
    :return:
    """
    data = {
        "code": "0000",
        "message": "操作成功",
        "request_id": "1234"
    }
    ret = entry_data(data, "1234")
    return jsonify(data)


@nkz.route('/pay/withdraw/withdraw/', methods=['POST'])
def withdraw():
    """
    提现接口
    :return:
    """
    data = {}
    ret = entry_data(data, "")
    return jsonify(ret)


@nkz.route('/api/payment/v1/query-accounts', methods=['GET'])
def query_accounts():
    """
    提现查询接口
    :return:
    """
    data = {
            "code": "0000",
            "data": {
                "dealer_infos": [
                    {
                        "alipay_balance": "0.00",
                        "bank_card_balance": "20.00",
                        "broker_id": "27532644",
                        "is_alipay": True,
                        "is_bank_card": True,
                        "is_wxpay": True,
                        "rebate_fee_balance": "0.00",
                        "wxpay_balance": "0.00"
                    }
                ]},
            "message": "操作成功",
            "request_id": "5c09171ac46bd"
    }
    # ret = entry_data(data, "")
    return jsonify(data)


@nkz.route('/api/payment/v1/order-realtime', methods=['POST'])
def order_realtime():
    """
    提现查询接口
    :return:
    """
    data = {
        "code": "0000",
        "data": {
            "order_id": "YUN2018120620375349521025",
            "pay": "72.07",
            "ref": "174572401051074944"
            },
        "message": "操作成功",
        "request_id": "5c0918214f8fd"
    }
    # ret = entry_data(data, "")
    return jsonify(data)


@nkz.route('/alimarket/bankaddress', methods=['POST'])
def bankaddress():
    """
    获取银行卡地址
    :return:
    """
    data = {
        "error_code": 0,
        "reason": "Succes",
        "result": {
            "bankname": "中国银行",
            "banknum": "1040000",
            "cardprefixnum": "621569",
            "cardname": "长城福农借记卡普卡",
            "cardtype": "银联借记卡",
            "cardprefixlength": "6",
            "cardlength": "19",
            "isLuhn": True,
            "bankurl": "http://www.boc.cn",
            "enbankname": "Bank of China",
            "abbreviation": "BOC",
            "bankimage": "http://auth.apis.la/bank/cb.png",
            "servicephone": "95566",
            "province": "湖北省",
            "city": "武汉"
        },
        "ordersign": "9b834f58cd11cdc6c168a8d5390fe921",
        "dp_cache_key": "该字段为网关添加，不属于原始响应字段"
    }
    # ret = entry_data(data, "")
    import json
    return json.dumps(data, ensure_ascii=False)


@nkz.route('/api/payment/v1/query-realtime-order', methods=['GET'])
def query_realtime_order():
    """
    提现查询接口
    :return:
    """
    print(request.values.get("data"))
    print(request.args.get("data"))
    print(request.form.get("data"))
    data = {
            "code": "0000",
            "data": {
                "order_id": "YUN2018120620375349521025",
                "pay": "72.07",
                "broker_id": "27532644",
                "dealer_id": "23665418",
                "real_name": "杨雪超",
                "card_no": "6437887646487964",
                "id_card": "370212196010172146",
                "status": "2",
                "status_detail": "251",
                "status_message": "打款失败",
                "status_detail_message": "身份证姓名不匹配",
                "sys_amount": "0.00",
                "broker_amount": "0.00",
                "tax": "0.00",
                "ref": "174572401051074944",
                "withdraw_platform": "bankpay",
                "created_at": "2018-12-06 20:37:54",
                "finished_time": "2018-12-06 20:37:54",
                "sys_fee": "0.00",
                "broker_fee": "0.00"
            },
            "message": "操作成功",
            "request_id": "5c09186b08d28"
        }
    # ret = entry_data(data, "")
    return jsonify(data)

