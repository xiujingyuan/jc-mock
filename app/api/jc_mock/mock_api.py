import codecs
import datetime
import os
import random
import time
import traceback

from flask import Flask, jsonify, request, current_app, json, Response
from urllib import request as url_request
import requests
from app.api.jc_mock import mock
from app import db, csrf
from app.models import KeyValueDb
from app.models.KeyValueDb import KeyValue
from app.models.LinkModel import Link
from app.models.MockModel import Mock
from app.models.SysProgramDb import SysProgram
from app.models.jihe.MobileDeviceDb import MobileDevice
import string


@mock.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Mock!'


@mock.route('/capital/ftp/download/<string:loan_channel>', methods=['GET', 'POST'])
def mock_statement_file(loan_channel):
    with codecs.open('statement', 'rb+') as statement:
        content = statement.read()
    return Response(content, content_type='application/octet-stream')


@mock.route('/lanzhou/haoyue/fileNameQuery', methods=['GET', 'POST'])
def mock_file_name():
    with codecs.open('statement1', 'rb+') as statement:
        content = statement.read()
    return jsonify(json.loads(content))


@mock.route('/changyin/changyin_junxin/api/repayment/apply', methods=['GET', 'POST'])
def mock_changyin_junxin():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/runlou/changyin_mingdonghua_rl/loan.assis.cy.repayment.apply', methods=['GET', 'POST'])
def mock_changyin_mingdonghua_rl():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/zhongzhirong/yumin_zhongbao/ym.repay.apply', methods=['GET', 'POST'])
def mock_yumin_zhongbao():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/zhongzhirong/yumin_zhongbao/ym.repay.plan', methods=['GET', 'POST'])
def mock_yumin_zhongbao_plan():
    ret = {"code": "0", "message": "成功", "data": {"planList": [{"currentArrears": 0, "interestAmount": 1953, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24117, "repayDate": "20230612", "rpyblCmpdInt": 0, "termNo": "1", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 1796, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24274, "repayDate": "20230712", "rpyblCmpdInt": 0, "termNo": "2", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 1638, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24432, "repayDate": "20230812", "rpyblCmpdInt": 0, "termNo": "3", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 1479, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24591, "repayDate": "20230912", "rpyblCmpdInt": 0, "termNo": "4", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 1318, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24752, "repayDate": "20231012", "rpyblCmpdInt": 0, "termNo": "5", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 1157, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 24913, "repayDate": "20231112", "rpyblCmpdInt": 0, "termNo": "6", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 995, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25075, "repayDate": "20231212", "rpyblCmpdInt": 0, "termNo": "7", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 832, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25238, "repayDate": "20240112", "rpyblCmpdInt": 0, "termNo": "8", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 668, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25402, "repayDate": "20240212", "rpyblCmpdInt": 0, "termNo": "9", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 502, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25568, "repayDate": "20240312", "rpyblCmpdInt": 0, "termNo": "10", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 336, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25734, "repayDate": "20240412", "rpyblCmpdInt": 0, "termNo": "11", "totalAmount": 28366, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}, {"currentArrears": 0, "interestAmount": 169, "invalidCouponAmount": 0, "loanNo": "DNS20231686636901", "otsndCmpdIntBal": 0, "otsndIntAmt": 0, "otsndPnpAmt": 0, "otsndPnyIntAmt": 0, "overdueDay": "0", "paymentFlag": "PR", "penaltyIntAmount": 0, "planNo": "", "principalAmount": 25904, "repayDate": "20240512", "rpyblCmpdInt": 0, "termNo": "12", "totalAmount": 28372, "totalTerm": "12", "unusedCouponAmount": 0, "usedCouponAmount": 0}]}}
    return jsonify(json.loads(ret))


@mock.route('/xinheyuan/jiexin_taikang_xinheyuan/repaymentApply', methods=['GET', 'POST'])
def mock_jiexin_taikang_xinheyuan():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/zhongbang/zhongbang_zhongji/normRpyOnTm', methods=['GET', 'POST'])
def mock_zhongbang_zhongji():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/qingjia/lanhai_zhongshi_qj/normalRepayApply', methods=['GET', 'POST'])
def mock_lanhai_zhongshi_qj():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))


@mock.route('/withhold/autoPay', methods=['GET', 'POST'])
def mock_autoPay():
    time.sleep(60)
    ret = {
          "code": 0,
          "message": "成功",
    }
    return jsonify(json.loads(ret))

@mock.route('/lanzhou/fileNameQuery', methods=['GET', 'POST'])
def mock_lan_file_name():
    with codecs.open('statement1', 'rb+') as statement:
        content = statement.read()
    return jsonify(json.loads(content))


@mock.route('/capital/ftp/upload/<string:loan_channel>', methods=['GET', 'POST'])
def mock_upload_statement_file(loan_channel):
    # print(request.stream)
    ret = {
      "code": 0,
      "message": "上传成功",
      "data": {
        "dir": "/11001/202107115/",
        "name": "xkltb20210715_L00021.txt",
        "type": None,
        "result": {
          "code": 0,
          "message": "成功"
        }
      }
    }
    return jsonify(ret)


@mock.route('/mozhibeiyin/repay.list', methods=['GET', 'POST'])
@csrf.exempt
def mock_mozhibeiyin_repay_list():
    get_key = KeyValue.query.filter(KeyValue.key == "mozhi_repay_list").first()
    if not get_key:
        raise ValueError("not fount the key's {0} config ".format("mozhi_repay_list"))
    outOrderNo = json.loads(get_key.value)['trade_no']
    is_ok = int(json.loads(get_key.value)['count'])
    ret_str = 'test' if is_ok % 2 == 1 else outOrderNo
    ret = {
          "code": 0,
          "message": "成功",
          "data": [{
            "preRepayPrincipal": 800000,
            "repayAmount": 60169,
            "bankName": "中国建设银行",
            "preRepayAmount": 816930,
            "cardNo": "5522458145187710",
            "preRepayFee": 0,
            "loanTime": 1619428012303,
            "preRepayOvdInterPenalty": 0,
            "currentTerm": 2,
            "preRepayInterest": 16930,
            "overdueDays": 0,
            "repayPlanItems": [{
              "termPrincipal": 55813,
              "termInterPenalty": 0,
              "shouldRepayDate": "20210526",
              "termAmount": 60169,
              "overdueDays": 0,
              "termPrinPenalty": 0,
              "termNo": 1,
              "termGuaranteeAmount": 0,
              "termInterest": 4356,
              "termFee": 0,
              "termInsuranceAmount": 0
            }],
            "repayInterest": 4356,
            "preGuaranteeAmount": 0,
            "termNum": 6,
            "prePenalty": 0,
            "insuranceAmount": 0,
            "repayPrincipal": 55813,
            "preInsuranceAmount": 0,
            "guaranteeAmount": 0,
            "abbreviation": "CCB",
            "outOrderNo": ret_str,
            "loanAmount": 600000,
            "preRepayOvdPrinPenalty": 0,
            "repayFee": 0,
            "repayDate": "20210526",
            "interPenalty": 0,
            "prinPenalty": 57,
            "status": "REPAY"
          }]
        }
    get_key.value = json.dumps({'trade_no': outOrderNo, 'count': (is_ok + 1)})
    db.session.flush()
    return jsonify(ret)


@mock.route('/link', methods=['POST', 'PUT'])
def add_link():
    """
    身份证实名验证接口
    :return:
    """
    if request.method == "POST":
        request_data = request.json
        if request_data is None:
            data = {"code": 1,
                    "msg": "请求参数不能为空"}
        elif 'link_type' in request_data.keys() and 'link_title' in request_data.keys() \
                and 'link_url' in request_data.keys():
            sys_program_name = request_data["link_type"]
            link_title = request_data["link_title"]
            link_url = request_data["link_url"]
            user = request_data["user"]
            pwd = request_data["pwd"]
            select_sys_program = SysProgram.query.filter_by(sys_program_name=sys_program_name).first()
            if select_sys_program is None:
                data = {"code": 1,
                        "msg": "链接类型未找到"}
            else:
                if not isinstance(sys_program_name, str):
                    data = {"code": 1,
                            "msg": "链接类型的参数类型错误"}
                elif not isinstance(link_title, str):
                    data = {"code": 1,
                            "msg": "链接名称的参数类型错误"}
                elif not isinstance(link_url, str):
                    data = {"code": 1,
                            "msg": "链接地址的参数类型错误"}
                elif user and not isinstance(user, str):
                    data = {"code": 1,
                            "msg": "用户名的参数类型错误"}
                elif pwd and not isinstance(pwd, str):
                    data = {"code": 1,
                            "msg": "密码的参数类型错误"}
                else:
                    try:
                        link = Link(link_title=link_title,
                                    link_url=link_url,
                                    link_type=select_sys_program.sys_program_id,
                                    link_user=user,
                                    link_pwd=pwd)
                        db.session.add(link)
                        db.session.flush()
                    except:
                        print(traceback.format_exc())
                        data = {"code": 1,
                                "msg": "添加链接异常"}
                    else:
                        data = {"code": 0,
                                "msg": "添加链接成功"}
        else:
            data = {"code": 1,
                    "msg": "参数错误，请检查"}
    elif request.method == "PUT":
        request_data = request.json
        if request_data is None:
            data = {"code": 1,
                    "msg": "请求参数不能为空"}
        elif 'link_id' in request_data.keys() and 'link_title' in request_data.keys() \
                and 'link_url' in request_data.keys():
            link_id = request_data["link_id"]

            link_title = request_data["link_title"]
            link_url = request_data["link_url"]
            user = request_data["user"]
            pwd = request_data["pwd"]
            link = Link.query.filter_by(link_id=link_id).first()
            if link is None:
                data = {"code": 1,
                        "msg": "此链接不存在，请检查"}
            else:
                select_sys_program = SysProgram.query.filter_by(sys_program_id=link.link_type).first()
                if select_sys_program is None:
                    data = {"code": 1,
                            "msg": "链接类型未找到"}
                else:
                    try:
                        link.link_url = link_url
                        link.link_type = select_sys_program.sys_program_id
                        link.link_user = user
                        link.link_pwd = pwd
                        link.link_title = link_title
                        
                    except:
                        print(traceback.format_exc())
                        data = {"code": 1,
                                "msg": "更新链接异常"}
                    else:
                        data = {"code": 0,
                                "msg": "更新链接成功"}

        else:
            data = {"code": 1,
                    "msg": "参数错误，请检查"}

    return jsonify(data)


@mock.route('/link_type', methods=['POST'])
def add_link_type():
    """
    身份证实名验证接口
    :return:
    """
    if request.method == "POST":
        request_data = request.json
        if request_data is None:
            data = {"code": 1,
                    "msg": "请求参数不能为空"}
        elif 'link_title' in request_data.keys():
            link_title = request_data["link_title"]
            select_link_type = SysProgram.query.filter_by(link_type_name=link_title).first()
            if select_link_type is not None:
                data = {"code": 1,
                        "msg": "链接类型已存在"}
            else:
                if not isinstance(link_title, str):
                    data = {"code": 1,
                            "msg": "链接名称的参数类型错误"}
                else:
                    try:
                        link_type = SysProgram(link_type_name=link_title)
                        db.session.add(link_type)
                        db.session.flush()
                    except:
                        data = {"code": 1,
                                "msg": "添加链接类型异常"}
                    else:
                        data = {"code": 0,
                                "msg": "添加链接类型成功"}
        else:
            data = {"code": 1,
                    "msg": "参数错误，请检查"}
    return jsonify(data)


@mock.route('/pre', methods=["PUT"])
def edit_pre():
    pre_data = {
        "result": 1,
        "message": "更新失败"
    }
    try:
        request_data = request.json
        case_pre_id = request_data["prev_id"]
    except:
        print(traceback.format_exc())
        pass
    else:
        try:
            get_case = url_request.urlopen('http://api.gaea.com/prev/id/{0}'.format(case_pre_id))
            # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
            result = get_case.read()
        except:
            print(traceback.format_exc())
            pass
        else:
            pre_data["result"] = 0
            pre_data["message"] = "获取成功"
            pre_data["data"] = json.loads(result)

    return jsonify(pre_data)


@mock.route('/init', methods=["DELETE"])
def del_init():
    request_data = request.json
    print(request_data["init_id"])
    data = {
        "result": 1,
        "message": "删除失败"
    }
    return jsonify(data)


@mock.route('/init/', methods=["PUT"])
def edit_init():
    init_data = {
        "result": 1,
        "message": "格式不正确"
    }
    try:
        request_data = request.json
        case_init_id = request_data["case_init_id"]
    except:
        print(traceback.format_exc())
        pass
    else:
        print(case_init_id)
        try:
            get_case = url_request.urlopen('http://api.gaea.com/init/id/{0}'.format(case_init_id))
            # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
            result = get_case.read()
        except:
            print(traceback.format_exc())
            pass
        else:
            init_data["result"] = 0
            init_data["message"] = "获取成功"
            init_data["data"] = json.loads(result)

    return jsonify(init_data)


@mock.route('/case/update', methods=["PUT"])
def case_update():
    case_update_data = {
        "result": 1,
        "message": "格式不正确"
    }
    try:
        request_data = request.json
    except:
        print(traceback.format_exc())
        pass
    else:
        send_data = {
                    "case": {
                        "basicInfo": request_data
                        }
                    }
        json_data = json.dumps(send_data).encode("utf-8")
        get_case = requests.put('http://api.gaea.com/case/{0}'.format(request_data["case_id"]),
                                       data=json_data,
                                       headers={"Content-Type": "application/json"})
        if get_case.status_code == 200:
            result = get_case.json()
            case_update_data["result"] = 0
            case_update_data["message"] = "获取成功"
            case_update_data["data"] = result
    return jsonify(case_update_data)


def random_device():
    ret = ""
    for i in range(len("8ce2f3103ac1")):
        num_or_zimu = random.randint(0, 1)
        if num_or_zimu == 1:
            ret += str(random.randint(0, 9))
        else:
            ret += random.choice(string.ascii_letters)
    return ret


def random_uin():
    ret = []
    for i in range(random.randint(0, 5)):
        random_type = random.randint(0, 2)
        if random_type == 0:
            ret.append("        <string></string>")
        elif random_type == 1:
            ret.append("        <string>{0}</string>".format(random.randint(10000000, 99999999)))
        else:
            ret.append("        <string>-{0}</string>".format(random_device()))
    return ret


@mock.route('/folder/create', methods=["GET"])
def create_device_folder():
    base_path = "/Users/snow/Desktop/wechat/"
    devices = MobileDevice.query.all()
    for device in devices:
        device_file = os.path.join(base_path, "{0}-{1}/shared_prefs/app_brand_global_sp.xml".format(device.imei, device.imei2))
        if not os.path.exists(os.path.dirname(device_file)):
            os.makedirs(os.path.dirname(device_file))
        with codecs.open(device_file, "w") as write_file:
            write_content = []
            write_content.append("<?xml version='1.0' encoding='utf-8' standalone='yes' ?>")
            write_content.append("<map>")
            write_content.append('    <set name="uin_set">')
            write_content += random_uin()
            write_content.append('    </set>')
            write_content.append('</map>')
            for item in write_content:
                write_file.write(item + "\n")
    return jsonify({"code": "success"})
