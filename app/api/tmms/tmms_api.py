from datetime import datetime

from flask import Flask, jsonify, request
import random

from app import csrf
from app.common.components.encrypt_request import entry_data
from app.api.tmms import tmms
import json
import time


@tmms.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World!'


@tmms.route('/api/identity/auth', methods=['POST'])
def identity_auth():
    """
    认证接口
    :return:
    """
    data = {
        "status": 0,
        "info": "SUCCESS",
        "time": 1540955716,
        "data": {
            "access_token": "b23abb6d451346efa13370172d1921ef",
            "expire_in": 7200
            }
        }
    return jsonify(data)


@tmms.route('/api/enterprise/getScripts', methods=['POST', 'GET'])
def verify_bankcard_three_factors():
    """
    获取企业话术列表接口
    :return:
    """
    data = {
            "status": 0,
            "info": "SUCCESS",
            "time": 1540955716,
            "data": [{
                "script_id": 1,
                "script_name": "性能测试话术",
                "create_time": 1540955716
            }]
        }
    return jsonify(data)


@tmms.route('/api/task/saveOutcallTask', methods=['POST'])
def save_out_call_task():
    """
    创建任务接口
    :return:
    """
    data = {
        "status": 0,
        "info": "SUCCESS",
        "time": 1540955716,
        "data": {
            "task_id": random.randint(4000, 9000)
        }
    }
    return jsonify(data)


@tmms.route('/api/task/importClues', methods=['POST'])
def import_clues():
    """
    任务中导入客户接口
    :return:
    """
    data = {}
    if request.method == "POST":
        print(request.json, type(request.json))
        request_data = request.json
        if 'task_id' in request_data.keys():
            task_id = request_data["task_id"]
            if task_id == "1":
                time.sleep(10)
            data = {
                    "status": 0,
                    "info": "SUCCESS",
                    "time": 1540955716,
                    "data": {
                        "num": 100,
                        "num_success": 90,
                        "num_failed": 10,
                        "reasons": [{
                            "clue": "1365517289",
                            "error": "线索号码不符合规则"
                        }]
                    }
                }
    return jsonify(data)


@tmms.route('/api/task/startOutcallTask', methods=['POST'])
def start_out_call_task():
    """
    启动任务接口
    :return:
    """
    data = {
            "status": 0,
            "info": "SUCCESS",
            "time": 1540955716,
            "data": ""
        }
    return jsonify(data)


@tmms.route('/api/task/deleteOutcallTask', methods=['POST'])
def delete_out_call_task():
    """
    删除任务接口
    :return:
    """
    data = {
            "status": 0,
            "info": "SUCCESS",
            "time": 1540955716,
            "data": ""
        }
    # ret = entry_data(data, "")
    return json.dumps(data, ensure_ascii=False)


@tmms.route('/api/task/pauseOutcallTask', methods=['POST'])
def pause_out_call_task():
    """
    暂停任务接口
    :return:
    """
    data = {
            "status": 0,
            "info": "SUCCESS",
            "time": 1540955716,
            "data": ""
        }
    # ret = entry_data(data, "")
    return json.dumps(data, ensure_ascii=False)


@tmms.route('/api/task/getTaskList', methods=['POST'])
def get_task_list():
    """
    获取任务列表接口
    :return:
    """
    data = {
            "status": 0,
            "info": "SUCCESS",
            "time": 1540955716,
            "data": {
                "count": 1000,
                "tasks": [{
                    "uuid": "121212",
                    "task_id": 1,
                    "task_name": "测试任务",
                    "script_name": "测试话术",
                    "task_status": 2,
                    "clue_num": 200,
                    "account_num": 10,
                    "create_time": 1540955716,
                    "start_time": 1540955716,
                    "complete_time": 1540955716
                }]
            }
        }
    return jsonify(data)


@tmms.route('/api/task/getCallRecordDetail', methods=['POST'])
def get_call_record_detail():
    """
    获取通话详情接口
    :return:
    """
    if request.method == "POST":
        print(request.json, type(request.json))
        request_data = request.json
        if request_data is not None and 'task_id' in request_data.keys() and 'clues' in request_data.keys():
            task_id = request_data["task_id"]
            phones = request_data["clues"]
            limit = request_data["limit"]
            data = {
                "status": 0,
                "info": "SUCCESS",
                "time": int(time.time()),
                "data": {
                    "count": limit,
                    "records": []
                }
            }
            # phones = ["15969021783"]
            for index, phone in enumerate(phones):
                if index >= 30:
                    break
                time_random = random.randint(1, 300)
                call_result = random.randint(0, 5)
                # manual_status = random.randint(0, 3)
                # call_result = 2
                manual_status = 0
                data_records = {
                    "task_id": task_id,
                    "script_name": "测试话术",
                    "callee_phone": phone,
                    "cc_number": "20017_00000010conf0_{0}".format(phone),
                    "calllog_txt": "<calllog>fdasfasdfsdfds67rewqrqwerqwr___sdfds__{0}__dsfs</calllog>".format(phone),
                    "call_result": call_result,
                    "call_progress": 2,
                    "call_time": 1540955716,
                    "duration": random.randint(1, 100),
                    "intention_type": 2,
                    "manual_status": manual_status,
                    "label": "跟进",
                    "call_count": random.randint(1, 3),
                    "record_url": "",
                    "answer_time": 1540955716 + time_random,
                    "hangup_time": 1540955716 + time_random + random.randint(0, 100),
                    "match_global_keyword": {
                        "年级": random.choice(("幼儿园", "小学", "初中", "高中", "大学", "硕士", "博士")),
                        "性别": random.choice(("男", "女"))
                    }
                }
                if call_result == 2 and manual_status == 2:
                    data_records["transfer_number"] = "{0}_000136e5".format(random.choice((1009, )))
                    data_records["transfer_duration"] = random.randint(1, 100)
                data["data"]["records"].append(data_records)
        else:
            data = {
                "status": 20003,
                "info": "Failed",
                "time": 1540955716,
                "data": []
            }

    return jsonify(data)


@tmms.route('/api/v1/autoCallTasks', methods=['POST'])
@csrf.exempt
def udesk_create_task():
    """
    获取udesk的任务详情接口
    :return:
    """
    request_data = request.json
    if request_data is not None and 'name' in request_data.keys() and 'type' in request_data.keys():

        task_name = request_data["name"]
        task_type = request_data["type"]
        task_startMode = request_data["startMode"]
        task_startTime = request_data["startTime"]
        task_scheduleId = request_data["scheduleId"]
        task_ivrRouterId = request_data["ivrRouterId"]
        task_calloutNumber = request_data["calloutNumber"]
        task_callLimit = request_data["callLimit"]
        task_redialScene = request_data["redialScene"]
        task_redialTimes = request_data["redialTimes"]
        task_redialGuide = request_data["redialGuide"]
        task_remark = request_data["remark"]
        task_customFieldTemplateId = request_data["customFieldTemplateId"]

        data = {"code": 200,
                "message": "SUCCESS",
                "visible": False,
                "data": {}
                }

        # {"code": 400, "message": "名称不能重复", "visible": True, "exception": None, "paging": None, "data": None,
        #  "extra": None}

        data["data"] = {
            "id": random.randint(1000, 50000),
            "name": task_name,
            "type": task_type,
            "startMode": task_startMode,
            "startTime": task_startTime,
            "scheduleId": task_scheduleId,
            "ivrRouterId": task_ivrRouterId,
            "calloutNumber": task_calloutNumber,
            "callLimit": task_callLimit,
            "redialScene": task_redialScene,
            "redialTimes": task_redialTimes,
            "redialGuide": task_redialGuide,
            "status": 1,
            "totalCount": 5,
            "execCount": 0,
            "callSuccessCount": 0,
            "remark": task_remark,
            "createTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customFieldTemplateId": task_customFieldTemplateId
          }
    else:
        data = {
            "status": 20003,
            "message": "Failed",
            "time": 1540955716,
            "data": []
        }

    return jsonify(data)


@tmms.route('/api/v1/autoCallTasks/status/start', methods=['GET', 'POST'])
@csrf.exempt
def udesk_start_task():
    """
    启动udesk的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
              "code": 200,
              "message": "OK",
              "visible": False
            }

    else:
        data = {
            "status": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/autoCallTasks/status/pause', methods=['GET', 'POST'])
@csrf.exempt
def udesk_pause_task():
    """
    暂停udesk的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
              "code": 200,
              "message": "OK",
              "visible": False
            }

    else:
        data = {
            "status": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/outboundCustomFieldTemplates', methods=['GET', 'POST'])
@csrf.exempt
def udesk_get_templates():
    """
    获取模版udesk的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
                  "code": 200,
                  "message": "OK",
                  "visible": False,
                  "exception": None,
                  "paging": {
                    "pageNum": 1,
                    "pageSize": 20,
                    "total": 1
                  },
                  "data": [
                    {
                      "id": 7,
                      "name": "问卷调查",
                      "enabled": 1
                    }
                  ],
                  "extra": None
                }

    else:
        data = {
            "status": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/autoCallTasks/syncNumber', methods=['GET', 'POST'])
@csrf.exempt
def udesk_sync_number():
    """
    上传电话号码_udesk_的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
            "code": 200,
            "message": None,
            "visible": False,
            "exception": None,
            "paging": None,
            "data": {
                "successCount": 1,
                "failedCount": 0,
                "failedNumberList": []
            },
            "extra": None
        }

    else:
        data = {
            "status": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/worktimes', methods=['GET', 'POST'])
@csrf.exempt
def udesk_work_times():
    """
    获取工作时间_udesk_的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
              "code": 200,
              "message": "OK",
              "visible": False,
              "exception": None,
              "paging": {
                "pageNum": 1,
                "pageSize": 100,
                "total": 5
              },
              "data": [
                {
                  "id": 66,
                  "name": "正常工作时间"
                },
                {
                  "id": 41,
                  "name": "AI工作时间"
                },
                {
                  "id": 26,
                  "name": "休息日"
                },
                {
                  "id": 23,
                  "name": "周三"
                },
                {
                  "id": 18,
                  "name": "一周7天"
                }
              ],
              "extra": None
            }
        # data["data"] = []
    else:
        data = {
            "code": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/speechTechniques', methods=['GET', 'POST'])
@csrf.exempt
def udesk_speechTechniques():
    """
    获取话术_udesk_的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
              "code": 200,
              "message": "OK",
              "visible": False,
              "exception": None,
              "paging": {
                "pageNum": 1,
                "pageSize": 31,
                "total": 31
              },
              "data": [
                {
                  "id": 2,
                  "name": "语音通知测试"
                },
                {
                  "id": 10,
                  "name": "银行贷款demo"
                },
                {
                  "id": 23,
                  "name": "dushiliren-test"
                },
                {
                  "id": 28,
                  "name": "YDZ-Demo"
                },
                {
                  "id": 32,
                  "name": "物流YN"
                },
                {
                  "id": 33,
                  "name": "dongyirisheng"
                },
                {
                  "id": 62,
                  "name": "bank_interrupt"
                },
                {
                  "id": 64,
                  "name": "dapinwenhuatest"
                },
                {
                  "id": 78,
                  "name": "银行打断"
                },
                {
                  "id": 83,
                  "name": "银行打断（副本）"
                },
                {
                  "id": 92,
                  "name": "SkyTest"
                },
                {
                  "id": 111,
                  "name": "诗华第一轮节假日"
                },
                {
                  "id": 115,
                  "name": "CH诗华二轮测试（副本）"
                },
                {
                  "id": 145,
                  "name": "凯斯软件（峰会邀请）"
                },
                {
                  "id": 146,
                  "name": "联通388"
                },
                {
                  "id": 153,
                  "name": "通通"
                },
                {
                  "id": 166,
                  "name": "kuainiu"
                },
                {
                  "id": 168,
                  "name": "入队"
                },
                {
                  "id": 169,
                  "name": "kuainiu2"
                },
                {
                  "id": 173,
                  "name": "凯斯软件（网页浏览呼出）"
                },
                {
                  "id": 175,
                  "name": "南昌新东方"
                },
                {
                  "id": 185,
                  "name": "变量Demo（JYB）"
                },
                {
                  "id": 188,
                  "name": "银行贷款demo打断（勿动）"
                },
                {
                  "id": 189,
                  "name": "银行贷款demo非打断（勿动）"
                },
                {
                  "id": 192,
                  "name": "银行练习--勿动"
                },
                {
                  "id": 193,
                  "name": "DTB变量DEMO"
                },
                {
                  "id": 196,
                  "name": "按键变量test"
                },
                {
                  "id": 198,
                  "name": "Qwert"
                },
                {
                  "id": 202,
                  "name": "快牛金科-贷上钱测试"
                },
                {
                  "id": 205,
                  "name": "凯斯（留言呼出）"
                },
                {
                  "id": 209,
                  "name": "入队9009"
                }
              ],
              "extra": None
            }

    else:
        data = {
            "code": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)


@tmms.route('/api/v1/spNumbers', methods=['GET', 'POST'])
@csrf.exempt
def udesk_spNumbers():
    """
    获取外呼号码_udesk_的任务详情接口
    :return:
    """
    if 'email' in request.args.keys():
        data = {
              "code": 200,
              "message": "OK",
              "visible": False,
              "exception": None,
              "paging": {
                "pageNum": 1,
                "pageSize": 2,
                "total": 2
              },
              "data": [
                {
                  "id": 3,
                  "number": "02566806102",
                  "name": "02566806102"
                },
                {
                  "id": 81,
                  "number": "02160781133",
                  "name": "02160781133"
                }
              ],
              "extra": None
            }

    else:
        data = {
            "code": 20003,
            "message": "Failed",
            "visible": False
        }

    return jsonify(data)
