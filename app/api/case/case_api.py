
import traceback
import json, os
import requests

from app import db
from app.api.case import api_case
from flask import jsonify, request, current_app, Response, render_template

from app.models.CommonToolsDb import CommonTool
from app.models.ProgramBusinessDb import ProgramBusiness
from app.models.SysProgramDb import SysProgram
from environment.common.config import Config


@api_case.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Case!'


@api_case.route('/case/', methods=['POST', 'PUT'])
def case():
    """
    创建用例，创建用例时，必须prev，init，mock，basicinfo 信息都要用
    更新用例，仅仅只是更新用例的basicinfo
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            # print(request_data)
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/case".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data": req.json()["data"]
                }
        else:
            request_data = request.json
            case_id = request_data["case_id"] if "flag" in request_data else request_data['case']['basicInfo']['case_id']
            url = "{0}/case/{1}".format(current_app.config["BACKEND_URL"], case_id)
            headers = {'content-type': 'application/json'}
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            current_app.logger.info(req)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                if not req.json()["data"]:
                    data["code"] = 0
                    data["msg"] = "success"
                    data["origin_data"] = req.json()["data"]
                else:
                    data["msg"] = req.json()["data"]
    except Exception as e:
        current_app.logger.exception(e)
        data["msg"] = str(e)
    return jsonify(data)


@api_case.route("/check_group", methods=["GET"])
def check_group():
    req = request.args
    print(req)
    url = "{0}/case/check_group".format(current_app.config["BACKEND_URL"])
    headers = {'content-type': 'application/json'}
    ret = requests.post(url, data=json.dumps(req), headers=headers)
    ret_data = {
        "code": 1,
        "msg": "查询失败"
    }
    if ret.status_code == 200:
        ret_data = ret.json()
    return jsonify(ret_data)


@api_case.route('/case/delete/<case_id>', methods=['DELETE'])
def delete_case(case_id):
    """
    通过case_id 删除用例，仅仅逻辑删除。设置case_status = -1
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "DELETE":
            url = "{0}/case/{1}".format(current_app.config["BACKEND_URL"],case_id)
            headers = {'content-type': 'application/json'}
            req = requests.delete(url,headers=headers)
            print(req.json())
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                data = {
                    "code": 0,
                    "msg": "success"
                }
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case/copy', methods=['POST'])
def case_copy():
    """
    复制用例(单个）
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/copy/group".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data": req.json()["data"]
                }
        print(data)
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case/copy_all', methods=['POST'])
def case_copy_all():
    """
    复制用例(单个）
    :return:
    """
    try:
        ret = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/case/copy_all".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                ret["code"] = 0
                ret["msg"] = "success"
    except Exception as e:
        current_app.logger.exception(e)
        ret["msg"] = e
        ret["code"] = 1
    finally:
        return jsonify(ret)


@api_case.route('/prev/add', methods=['POST'])
def add_prev():
    """
    单独添加前置数据。
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            current_app.logger.info(request_data)
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/prev".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            print(req.json())
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data": req.json()['data'][0]
                }
            current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/history_pre/<int:case_id>/<string:build_id>', methods=['GET'])
def get_history_prev(case_id, build_id):
    """
    根据用例ID获取执行后的前置条件
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        # print(type(request_data))
        # print(json.dumps(request_data, ensure_ascii=False))
        url = "{0}/history_prev/{1}/{2}".format(current_app.config["BACKEND_URL"], case_id, build_id)
        headers = {'content-type': 'application/json'}
        req = requests.get(url, headers=headers)
        print(req.json())
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            data = {
                "code": 0,
                "msg": "success",
                "rows": req.json()['data'],
                "total": len(req.json()['data'])
            }
        current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/history_init/<int:case_id>/<string:build_id>', methods=['GET'])
def get_history_init(case_id, build_id):
    """
    根据用例ID获取执行后的前置条件
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        url = "{0}/history_init/{1}/{2}".format(current_app.config["BACKEND_URL"], case_id, build_id)
        headers = {'content-type': 'application/json'}
        req = requests.get(url, headers=headers)
        print(req.json())
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            data = {
                "code": 0,
                "msg": "success",
                "rows": req.json()['data'],
                "total": len(req.json()['data'])
            }
        current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/init/add', methods=['POST'])
def add_init():
    """
    单独添加初始化数据。
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            current_app.logger.info(request_data)
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/init".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            print(req.json())
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data": req.json()['data'][0]
                }
        current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/run/case', methods=['POST'])
def run_case():
    """
   运行用例，后台会将这个用例交给jenkins 执行。
   :return:
   """
    try:
        data = {
            "code": 1,
            "msg": "请求后台任务失败，请联系管理员"
        }
        if request.method == "POST":
            request_data = request.json
            url = "{0}/run/case".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            current_app.logger.info(request_data)
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json():
                result = req.json()
                data = {
                    "code": result['code'],
                    "msg": result['msg'],
                    "origin_data": result['data']
                }
        current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/search/', methods=['GET', 'POST'])
def search():
    """
    搜索用例。
    :return:
    """
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "total": 0,
            'rows': []
        }

        if request.method == "GET":
            request_data = request.args
            json_data = {}
            url = "{0}/case/search".format(current_app.config["BACKEND_URL"])
            current_app.logger.info(url)
            api_log = Apilog()
            api_log.apilog_url = url
            db.session.add(api_log)
            db.session.flush()
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(request_data)
            json_data = json.loads(json_data)
            json_data["page_index"] = int(json_data["page_index"])
            json_data["page_size"] = int(json_data["page_size"])
            current_app.logger.info(json_data)
            req = requests.post(url, data=json.dumps(json_data), headers=headers)
            current_app.logger.info(req)
            current_app.logger.info(req.json())
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                req_data = req.json()
                current_app.logger.info(req_data)
                if "data" in req_data and "cases" in req_data["data"]:
                    data["code"] = 0
                    data["message"] = "查询成功"
                    sys_programs = get_sys_program()
                    def get_cname(sys_program_id):
                        for program in sys_programs:
                            if program["sys_program_id"] == sys_program_id:
                                return program["sys_program_name"]
                        return ""

                    all_business = ProgramBusiness.query.all()

                    def get_business_name(sys_program_id, business_name):
                        for business in all_business:
                            if business.program_id == sys_program_id and business.business_name == business_name:
                                return business.business_cname
                        return ""

                    search_cases = req_data["data"]["cases"]
                    for item_case in search_cases:
                        item_case["case_from_system_name"] = get_cname(item_case["case_from_system"])
                        item_case["case_belong_business_name"] = get_business_name(item_case["case_from_system"],
                                                                                   item_case["case_belong_business"]
                                                                                   )
                    data["rows"] = search_cases
                    data["total"] = req_data["data"]["total"]

        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/search/variable/', methods=['POST','GET'])
def system_variable():
    '''
    搜索系统变量
    :return:
    '''
    try:
        data ={
            "total": 0,
            'rows': []
        }
        if request.method == 'GET':
            request_data = request.args
            url = "{0}/params/search".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(request_data)
            json_data = json.loads(json_data)
            json_data["page_index"] = int(json_data["page_index"])
            json_data["page_size"] = int(json_data["page_size"])
            current_app.logger.info(json_data)
            req = requests.post(url, data=json.dumps(json_data), headers=headers)

            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                req_data = req.json()
                if "data" in req_data and "params" in req_data["data"]:
                    data["rows"] = req_data["data"]["params"]
                    data["total"] = req_data["data"]["total"]
            current_app.logger.info(data)
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/variable/add/", methods=['POST'])
def add_variable():
    """
    创建系统变量
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            url = "{0}/params".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            current_app.logger.info(request_data)
            req = requests.post(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data":request_data
                }
            current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/prev/update/", methods=['PUT'])
def update_prev():
    """
    更新前置处理
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "PUT":
            request_data = request.json
            # print(type(request_data))
            prev_id = request_data['prev_id']
            url = "{0}/prev/{1}".format(current_app.config["BACKEND_URL"],prev_id)
            headers = {'content-type': 'application/json'}
            current_app.logger.info(request_data)
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data":request_data
                }
            current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/init/update/", methods=['PUT'])
def update_init():
    """
    更新初始化数据
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "PUT":
            request_data = request.json
            # print(type(request_data))
            print(json.dumps(request_data, ensure_ascii=False))
            init_id = request_data['case_init_id']
            url = "{0}/init/{1}".format(current_app.config["BACKEND_URL"],init_id)
            headers = {'content-type': 'application/json'}
            print(request_data)
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data":request_data
                }
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/variable/update/", methods=['PUT'])
def update_variable():
    """
    更新系统变量
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "PUT":
            request_data = request.json
            id = request_data['id']
            url = "{0}/params/{1}".format(current_app.config["BACKEND_URL"],str(id))
            headers = {'content-type': 'application/json'}
            current_app.logger.info(id)
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "msg": "success",
                    "origin_data":request_data
                }
        current_app.logger.info(data)
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/variable/delete/", methods=['PUT'])
def delete_variable():
    """
    删除系统变量
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "PUT":
            request_data = request.json
            # print(type(request_data))
            # print(json.dumps(request_data, ensure_ascii=False))
            if "id" in request_data:
                id = request_data['id']
                url = "{0}/params/{1}".format(current_app.config["BACKEND_URL"],str(id))
                headers = {'content-type': 'application/json'}

                req = requests.put(url, data=json.dumps(request_data), headers=headers)
                current_app.logger.info(req.json())
                if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                    data = {
                        "code": 0,
                        "msg": "success"
                    }
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route("/variable/id/", methods=['POST'])
def get_variable_byid():
    """
    通过ID 获取系统变量
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        if request.method == "POST":
            request_data = request.json
            id = request_data['id']
            url = "{0}/params/{1}".format(current_app.config["BACKEND_URL"],str(id))
            headers = {'content-type': 'application/json'}
            req = requests.get(url, data=json.dumps(request_data), headers=headers)

            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:

                data = {
                    "code": 0,
                    "data": req.json()["data"]
                }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case_prev_edit/<pre_id>', methods=['GET'])
def case_pre_edit(pre_id):
    """
   获取单个前置处理数据
   :return:
   """

    try:
        headers = {'content-type': 'application/json'}
        init_entity = requests.get('{0}/prev/id/{1}'.format(current_app.config["BACKEND_URL"],pre_id),headers=headers)
        # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
        result = init_entity.json()
        if "code" in result and "data" in result:
            if result["code"] == 0:
                if result["data"] is not None:
                    data={
                        "code":0,
                        "data":result["data"][0]
                    }
                    return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case_init_edit/<case_init_id>', methods=['GET'])
def case_init_edit(case_init_id):
    """
  获取单个前置处理数据
  :return:
  """

    try:
        print(case_init_id)
        init_entity = requests.get('{0}/init/id/{1}'.format(current_app.config["BACKEND_URL"],case_init_id))
        # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
        result = init_entity.json()

        if "code" in result and "data" in result:
            if result["code"] == 0:
                if result["data"] is not None:
                    data = {
                        "code": 0,
                        "data": result["data"][0]
                    }

                    return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case_prev_edit/delete/<prev_id>', methods=['DELETE'])
def delete_case_prev(prev_id):
    """
  删除前置处理数据
  :return:
  """

    try:
        url = '{0}/prev/{1}'.format(current_app.config["BACKEND_URL"],prev_id)
        req = requests.delete(url)
        print(req.json())
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            data = {
                "code": 0,
                "msg": "success"
            }
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/case_init_edit/delete/<case_init_id>', methods=['DELETE'])
def delete_case_init(case_init_id):
    """
    删除初始化数据
    :return:
    """

    try:
        url = '{0}/init/{1}'.format(current_app.config["BACKEND_URL"],case_init_id)
        req = requests.delete(url)
        print(req.json())
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            data = {
                "code": 0,
                "msg": "success"
            }
        return jsonify(data)
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/history/search/', methods=['GET', 'POST'])
def history_search():
    '''
    查询执行日志
    '''
    try:
        data = {
            "code": 1,
            "msg": "failed"
        }
        request_data = None
        if request.method == "GET":
            request_data = request.args

        elif request.method=="POST":
            request_data = request.json

        json_data = {}
        url = "{0}/history/search".format(current_app.config["BACKEND_URL"])
        headers = {'content-type': 'application/json'}
        json_data = json.dumps(request_data)
        json_data = json.loads(json_data)
        json_data["page_index"] = int(json_data["page_index"])
        json_data["page_size"] = int(json_data["page_size"])
        current_app.logger.info(json_data)
        req = requests.post(url, data=json.dumps(json_data), headers=headers)
        if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
            req_data = req.json()
            if "data" in req_data and "cases" in req_data["data"]:
                data["code"] = 0
                data["message"] = "查询成功"
                data["rows"] = req_data["data"]["cases"]
                data["total"] = req_data["data"]["total"]

        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/common/get_tool', methods=['GET'])
def get_tools():
    """
    查询执行日志
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "请求失败"
        }

        tools = CommonTool.query.filter(CommonTool.common_tools_is_int == 1).all()
        data['code'] = 0
        data['msg'] = '请求成功'
        data['data'] = CommonTool.serialize_list(tools)
    except Exception as e:
        current_app.logger.exception(e)
        data["msg"] = e
    return Response(json.dumps(data), mimetype='application/json')


@api_case.route('/common/request', methods=['POST'])
def common_tools():
    """
    查询执行日志
    :return:
    """
    try:
        data = {
            "code": 1,
            "msg": "请求失败"
        }

        request_data = request.json

        url = request_data['common_tools_address']
        headers = {'content-type': 'application/json'}
        method = request_data['common_tools_method']
        json_data = request_data['common_tools_placeholder']
        json_data = json_data if isinstance(json_data, dict) else json.loads(json_data)
        if method == "POST":
            req = requests.post(url, json=json_data, headers=headers)
        else:
            req = requests.get(url, json=json_data, headers=headers)
        if req.status_code == 200:
            data["msg"] = json.loads(req.text)
            if "code" in data["msg"] and data["msg"]["code"] == 0:
                data["code"] = 0
        else:
            current_app.logger.error(req)
            data["msg"] = json.dumps(req.text)
    except Exception as e:
        current_app.logger.exception(e)
        data["msg"] = e
    return Response(json.dumps(data), mimetype='application/json')


@api_case.route('/load/case/<int:case_id>', methods=['GET'])
def load_case(case_id):
    '''
    初始化case_edit 页面
    :param :
    :return:
    '''
    data = {
        "code": 1,
        "message": "请求失败"
    }

    try:
        json_result = requests.get('{0}/case/{1}'.format(current_app.config["BACKEND_URL"], case_id))
        json_result = json_result.json()
    except:
        current_app.logger.exception(traceback.format_exc())
        data["message"] = traceback.format_exc()
    else:
        if "code" in json_result and "data" in json_result and \
                json_result["code"] == 0 and json_result["data"] is not None:
            data["result"] = json_result["data"]
            data["code"] = 0
            data["message"] = "查询成功"
    return Response(json.dumps(data), mimetype='application/json')


@api_case.route('/summary/case', methods=['GET'])
def summary_case():
    '''
    查询页面的弹出框统计api
    :param :
    :return:
    '''
    data = {
        "code": 1,
        "msg": "请求失败"
    }

    try:
        json_result = requests.get('{0}/summary/search'.format(current_app.config["BACKEND_URL"]))
        json_result =json_result.json()
        print(json_result)
    except:
        current_app.logger.exception(traceback.format_exc())
        pass
    else:
        if "code" in json_result and "data" in json_result:
            if json_result["code"] == 0:
                if json_result["data"] is not None:
                    case = json_result["data"]
        data["code"] = 0
        data["message"] = "查询成功"
        data["result"] = case
    return Response(json.dumps(data),mimetype='application/json')


@api_case.route('/copy/group', methods=['POST'])
def copy_group():
    '''
    复制复杂场景的用例，以及非复杂场景的用例，在case 搜索页面
    :param :
    :return:
    '''
    data = {
        "code": 1,
        "message": "复制用例失败"
    }

    try:
        request_data = request.json
        print(request_data)
        headers = {'content-type': 'application/json'}
        url = '{0}/copy/group'.format(current_app.config["BACKEND_URL"])
        res = requests.post(url, data=json.dumps(request_data), headers=headers)
        result = res.json()
    except:
        current_app.logger.exception(traceback.format_exc())
        pass
    else:
        if "code" in result and "data" in result:
            if result["code"] == 0:
                data["code"] = 0
                data["message"] = "复制成功"
            else:
                data["message"]=result["msg"]
    return Response(json.dumps(data),mimetype='application/json')


@api_case.route('/save/report-basic-info',methods=['POST'])
def save_report_basic_info():
    try:
        data = {
            "code": 1,
            "message": ""
        }
        report = request.json
        current_app.logger.info(report)
        headers = {'content-type': 'application/json'}
        url = '{0}/report/write-report'.format(current_app.config["BACKEND_URL"])
        result = requests.post(url, data=json.dumps(report), headers=headers).json()
        current_app.logger.info(result)
        if "code" in result and "data" in result:
            if result["code"] == 0:
                data["code"] = 0
                data["message"] = "保存成功"
            else:
                data["message"]=result["msg"]
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/upload/file', methods=['POST'])
def upload_save_file():
    try:
        data = {
            "code": 1,
            "message": ""
        }

        if 'upfile' in request.files:
            file = request.files['upfile']
        if 'branch_name' in request.form:
            branch_name = request.form['branch_name']
        if 'system_name' in request.form:
            system_name = request.form['system_name']
        if 'data' in request.form:
            report = request.form['data']
        if 'trans' in request.form:
            trans = request.form['trans']
        current_app.logger.info(report)
        current_app.logger.info(trans)
        filename_ext = file.filename
        current_app.logger.info(filename_ext)

        if '.' in filename_ext :
            #filename = secure_filename(filename_ext)
            filename = filename_ext
            path = os.path.join(Config.IMAGE_URL,system_name,branch_name)
            if os.path.exists(path)==False:
                os.makedirs(path)
            file.save(os.path.join(path,filename))
            link_filename = os.path.join(system_name,branch_name,filename).replace("\\","/")
            current_app.logger.info(Config.IMAGE_LINK_URL+link_filename)
            trans =json.loads(trans,encoding='utf-8')
            report = json.loads(report,encoding='utf-8')
            trans['finlab_report_transaction_image_url'] = link_filename
            trans_array = []
            trans_array.append(trans)
            report ={
                "report":report['report'],
                "trans":trans_array
            }
            headers = {'content-type': 'application/json'}
            url = '{0}/report/write-report'.format(current_app.config["BACKEND_URL"])
            result = requests.post(url, data=json.dumps(report), headers=headers).json()
            print(result)
            if "code" in result and "data" in result:
                if result["code"] == 0:
                    data["code"] = 0
                    data["message"] = "上传成功"
                    data["image_url"] = os.path.join(Config.IMAGE_LINK_URL,link_filename)
                else:
                    data["message"]=result["msg"]

        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/capture/screen', methods=['POST'])
def capture_report_screen():
    '''
    复制复杂场景的用例，以及非复杂场景的用例，在case 搜索页面
    :param :
    :return:
    '''
    data = {
        "code": 1,
        "message": "抓取图片失败"
    }

    try:
        request_data = request.json
        if 'data' in request_data.keys():
            report = request_data['data']
        if 'trans' in request_data.keys():
            trans = request_data['trans']
        if 'branch_name' in request_data.keys():
            branch_name = request_data['branch_name']
        if 'system_name' in request_data.keys():
            system_name = request_data['system_name']
        if 'image_name' in request_data.keys():
            image_name = request_data['image_name']
        path = os.path.join(Config.IMAGE_URL,system_name,branch_name)
        pathfile = os.path.join(path,image_name)
        if os.path.exists(path)==False:
            os.makedirs(path)
        report = json.loads(report,encoding='utf-8')
        trans = json.loads(trans,encoding='utf-8')
        request_data['path'] =pathfile
        trans_array = []
        image_url = os.path.join(system_name,branch_name,image_name)
        trans['finlab_report_transaction_image_url']=image_url.replace("\\","/")
        trans_array.append(trans)
        request_data['report'] =report['report']
        request_data['trans'] = trans_array
        del request_data['data']
        headers = {'content-type': 'application/json'}
        url = '{0}/report/capturescreen'.format(current_app.config["BACKEND_URL"])
        res = requests.post(url, data=json.dumps(request_data), headers=headers)
        result = res.json()
        if "code" in result and "data" in result:
            if result["code"] == 0:
                data["code"] = 0
                data['image_url']=os.path.join(Config.IMAGE_LINK_URL,image_url)
                data["message"] = "抓取图片成功"
            else:
                data["message"]=result["msg"]
        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/send/report', methods=['POST'])
def generate_report_html():
    '''
    发送测试报告邮件
    :param :
    :return:
    '''
    data = {
        "code": 1,
        "message": "发送测试报告失败"
    }
    try:
        result=""
        url = '{0}/report/report-detail'.format(current_app.config["BACKEND_URL"])
        header ={"content-type":"application/json"}
        data = request.json
        current_app.logger.info(data)
        req = requests.post(url,data=json.dumps(data),headers=header)
        report = req.json()
        if req.status_code == 200 and "code" in report and report["code"] == 0:
            master = report['data']
            trans = report['data']['trans']
            download_case_url=None
            for tran in trans:
                if tran['finlab_report_transaction_type']=="test_case":
                    download_case_url=tran['finlab_report_transaction_image_url']
                    current_app.logger.info(download_case_url)
            result = render_template(current_app.config["THEME_URL"] +'case/report-template.html', data=master, base_url=Config.IMAGE_LINK_URL, download_case_url = download_case_url)
            current_app.logger.info(result)
        else:
            current_app.logger.info(report)
            return Response(json.dumps(data),mimetype='application/json')
        master['finlab_report_content'] = result
        to_email = master['finlab_report_notify_address']
        system_name =  master['finlab_report_system_name']
        branch_name = master['finlab_report_branch_name']
        mail_title = "(info)系统:{0},分支:{1},测试报告".format(system_name,branch_name)
        mail = {
            "to_mail":to_email,
            "mail_title":mail_title,
            "content":result
        }
        email_url = '{0}/common/sendmail'.format(current_app.config["BACKEND_URL"])
        result_email = requests.post(email_url,data=json.dumps(mail),headers=header).json()
        if "code" in result_email and "data" in result_email:
            if result_email["code"] == 0:
                data["code"] = 0
                data["message"] = "发送邮件成功"
            else:
                data["message"]=result_email["msg"]
                return Response(json.dumps(data),mimetype='application/json')

        report_callback = {
            "report":master,
            "trans":[]
        }
        call_back_url= '{0}/report/write-report'.format(current_app.config["BACKEND_URL"])
        result_callback = requests.post(call_back_url, data=json.dumps(report_callback), headers=header).json()
        if "code" in result_callback and "data" in result_callback:
            if result_callback["code"] == 0:
                data["code"] = 0
                data["message"] = "发送邮件成功"
            else:
                data["message"]=result_callback["msg"]

        return Response(json.dumps(data),mimetype='application/json')

    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/report/search', methods=['GET'])
def search_report():
    """
    搜索报告。
    :return:
    """
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "total": 0,
            'rows': []
        }

        if request.method == "GET":
            request_data = request.args
            url = "{0}/report/search".format(current_app.config["BACKEND_URL"])
            api_log = Apilog()
            api_log.apilog_url = url
            db.session.add(api_log)
            db.session.flush()
            headers = {'content-type': 'application/json'}
            json_data = json.dumps(request_data)
            json_data = json.loads(json_data)
            if 'page_index' in json_data.keys():
                json_data["page_index"] = int(json_data["page_index"])
            else:
                json_data["page_index"] =1
            if 'page_size' in json_data.keys():
                json_data["page_size"] = int(json_data["page_size"])
            else:
                json_data["page_size"]=10
            current_app.logger.info(json_data)
            req = requests.post(url, data=json.dumps(json_data), headers=headers).json()
            current_app.logger.info(req)
            if "code" in req and req["code"] == 0:
                if "data" in req and "cases" in req["data"]:
                    data["code"] = 0
                    data["message"] = "查询成功"
                    data["rows"] = req["data"]["cases"]
                    data["total"] = req["data"]["total"]

        return Response(json.dumps(data),mimetype='application/json')
    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/report/detail', methods=['POST'])
def get_report_detail():
    """
    搜索报告。
    :return:
    """
    try:
        data = {
            "code": 1,
            "message": "查询错误",
        }

        request_data = request.json
        url = "{0}/report/report-detail".format(current_app.config["BACKEND_URL"])
        api_log = Apilog()
        api_log.apilog_url = url
        db.session.add(api_log)
        db.session.flush()
        headers = {'content-type': 'application/json'}
        current_app.logger.info(request_data)
        req = requests.post(url, data=json.dumps(request_data), headers=headers).json()
        current_app.logger.info(req)
        if "code" in req and req["code"] == 0:
            if "data" in req:
                data["code"] = 0
                data["message"] = "查询成功"
                data["rows"] = req["data"]
            return Response(json.dumps(data),mimetype='application/json')

    except Exception as e:
        current_app.logger.exception(e)


@api_case.route('/last_case/', methods=['GET'])
def get_new_cases():
    """
    获取最新更新的用例
    :return:
    """
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "data": []
        }
        url = "{0}/case/last_case".format(current_app.config["BACKEND_URL"])
        headers = {'content-type': 'application/json'}
        req = requests.get(url, headers=headers).json()
        current_app.logger.info(req)
        sys_programs = get_sys_program()

        def get_cname(sys_program_id):
            for program in sys_programs:
                if program["sys_program_id"] == sys_program_id:
                    return program["sys_program_name"]
            return ""

        if "code" in req and req["code"] == 0:
            if "data" in req:
                data["code"] = 0
                data["message"] = "查询成功"
                for item_case in req["data"]:
                    item_case["case_from_system_name"] = get_cname(item_case["case_from_system"])
                data["rows"] = req["data"]
    except Exception as e:
        current_app.logger.exception(e)
    finally:
        return jsonify(data)


def get_sys_program():
    if current_app.app_redis.exists("jc-sys_programs"):
        sys_programs = json.loads(current_app.app_redis.get("jc-sys_programs"))
    else:
        sys_programs = SysProgram.query.all()
        sys_programs = list(map(lambda x: x.serialize(), sys_programs))
        for sys_pro in sys_programs:
            sys_pro["sys_organization"] = sys_pro["sys_organization"].serialize()
            sys_pro["sys_organization"].pop("sys_organizations")
        current_app.app_redis.set("jc-sys_programs", json.dumps(sys_programs))
    return sys_programs


@api_case.route('/history/last_update', methods=['GET'])
def get_run_cases():
    """
    获取最新执行的用例
    :return:
    """
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "data": []
        }
        url = "{0}/history/last_update".format(current_app.config["BACKEND_URL"])
        headers = {'content-type': 'application/json'}
        req = requests.get(url, headers=headers).json()
        current_app.logger.info(req)
        if "code" in req and req["code"] == 0:
            if "data" in req:
                data["code"] = 0
                data["message"] = "查询成功"
                data["rows"] = req["data"][0]
    except Exception as e:
        current_app.logger.exception(e)
    finally:
        return jsonify(data)


@api_case.route('/all', methods=["GET", "POST"])
def get_all_case():
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "data": []
        }
        url = "{0}/case/all".format(current_app.config["BACKEND_URL"])
        headers = {'content-type': 'application/json'}
        print(request.args)
        req = requests.get(url, params=request.args, headers=headers).json()
        current_app.logger.info(req)
        if "code" in req and req["code"] == 0:
            if "data" in req:
                data["code"] = 0
                data["message"] = "查询成功"
                data["data"] = req["data"]
    except Exception as e:
        current_app.logger.exception(e)
    finally:
        return jsonify(data)


@api_case.route('/program_business/<int:program_id>', methods=["GET"])
def get_program_business(program_id):
    try:
        data = {
            "code": 1,
            "message": "查询错误",
            "data": []
        }
        program_business = ProgramBusiness.query.filter(ProgramBusiness.program_id == program_id).all()
        if program_business:
            data["code"] = 0
            data["message"] = "查询成功"
            data["data"] = ProgramBusiness.serialize_list(program_business)
    except Exception as e:
        current_app.logger.exception(e)
        data["message"] = str(e)
    finally:
        return jsonify(data)


@api_case.route('/add_business', methods=["POST"])
def add_business():
    try:
        data = {
            "code": 1,
            "message": "添加业务失败",
            "data": []
        }

        req = request.json
        if "project_id" not in req:
            data["message"] = "project_id不能为空"
        elif "business_name" not in req:
            data["message"] = "business_name不能为空"
        elif "business_cname" not in req:
            data["message"] = "business_cname不能为空"
        elif "autor" not in req:
            data["message"] = "autor不能为空"
        else:
            program_business = ProgramBusiness()
            program_business.program_id = req["project_id"]
            program_business.business_cname = req["business_cname"]
            program_business.business_name = req["business_name"]
            program_business.create_autor = req["autor"]
            db.session.add(program_business)
            db.session.flush()
            data["code"] = 0
            data["message"] = "添加业务成功"
    except Exception as e:
        current_app.logger.exception(e)
        data["message"] = str(e)

    finally:
        return jsonify(data)


@api_case.route('/prev_priority', methods=["PUT"])
def update_prev_priority():
    try:
        data = {
            "code": 1,
            "msg": "failed",
            "data": []
        }
        if request.method == "PUT":
            request_data = request.json
            url = "{0}/prev_priority".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                data["code"] = 0
                data["msg"] = "success",
                data["data"] = request_data
    except Exception as e:
        current_app.logger.exception(e)
    finally:
        return jsonify(data)


@api_case.route('/init_priority', methods=["PUT"])
def update_init_priority():
    try:
        data = {
            "code": 1,
            "msg": "failed",
            "data": []
        }
        if request.method == "PUT":
            request_data = request.json
            url = "{0}/init_priority".format(current_app.config["BACKEND_URL"])
            headers = {'content-type': 'application/json'}
            req = requests.put(url, data=json.dumps(request_data), headers=headers)
            if req.status_code == 200 and "code" in req.json() and req.json()["code"] == 0:
                data["code"] = 0
                data["msg"] = "success",
                data["data"] = request_data
    except Exception as e:
        current_app.logger.exception(e)
    finally:
        return jsonify(data)

@api_case.route('/my_test', methods=["GET"])
def my_test():
    test = {"amount": "702.10",
            "compensationFee": "2.04",
            "penalty": "0.00",
            "paybackType": "0",
            "payRemark": None,
            "partnerManagerFee": "34.25",
            "principal": "651.73",
            "creditId": "BIZ231770229200307120056",
            "prepayTerm": "2",
            "serialId": "ZJF405070182015205862",
            "interest": "50.37",
            "payChannel": "1",
            "withdrawTime": "2020 - 05 - 07 18: 30:23",
            "status": 1
        }

    data = {"retCode": 200,
            "retMsg": "操作成功",
            "data": '{"amount":"702.10","compensationFee":"2.04","penalty":"0.00","paybackType":"0","payRemark":null,'
                    '"partnerManagerFee":"34.25","principal":"651.73","creditId":"BIZ231770229200307120056",'
                    '"prepayTerm":"2","serialId":"ZJF405070182015205862","interest":"50.37","payChannel":"1",'
                    '"withdrawTime":"2020 - 05 - 07 18: 30:23","status":1}',
            "sign": "qVqLBGB5x42ZzjYnAJOOSSjJ1EGTtpH5jTlr3QPWVrVXLYkuqHZ=",
            "timestamp": "1588847440"
            }

    test_data = {
        "retCode": 200,
        "retMsg": "操作成功",
        "data": "",
        "sign": "qVqLBGB5x42ZzjYnAJOOSSjJ1EGTtpH5jTlr3QPWVrVXLYkuqHZ=",
        "timestamp": "1588847440"
    }

    test_data["data"] = test

    print(json.dumps(test_data, ensure_ascii=False))
    ret = {"success":1}
    return jsonify(ret)