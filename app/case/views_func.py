import traceback,requests
from flask import Flask, jsonify,current_app
from urllib import request
from flask import render_template, json
from flask_login import login_required

from app.base.views import BaseView
from app.case import case
from environment.common.config import Config

global_url = Config.BACKEND_URL


@case.route('/case', methods=['GET', 'POST'])
@login_required
def index():
    return render_template(current_app.config["THEME_URL"] +'case/cases.html')


@case.route('/add_case', methods=['GET'])
@login_required
def add_case():
    import time
    return render_template(current_app.config["THEME_URL"] +'case/case_add.html')


@case.route('/case/<int:case_id>/', methods=['GET'])
@login_required
def add_case_new(case_id):
    case = {}
    try:
        get_case = request.urlopen('{0}/case/{1}'.format(global_url,case_id))
        # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
        result = get_case.read()

    except:
        current_app.logger.exception(traceback.format_exc())
        pass
    else:
        json_result = json.loads(result)
        if "code" in json_result and "data" in json_result:
            if json_result["code"] == 0:
                if json_result["data"] is not None:
                    case = json_result["data"]


    # if not case:
    #     return render_template(current_app.config["THEME_URL"] +'403.html')
    # else:
    #     for initInfo in case["initInfo"]:
    #         initInfo["case_init_sql"] = ""
    #     for prevInfo in case["prevInfo"]:
    #         prevInfo["prev_sql_statement"] = ""
    #     case = json.dumps(case)
    #     return render_template(current_app.config["THEME_URL"] +'case/case_edit.html', case=case)
    # case = json.dumps(case)
    prevInfo = case['prevInfo']
    initInfo = case['initInfo']
    return render_template(current_app.config["THEME_URL"] +'case/case_edit.html', case=case, prevInfo = prevInfo,initInfo = initInfo)


@case.route('/case_system_variable/', methods=['GET'])
@login_required
def case_system_variable():
    return render_template(current_app.config["THEME_URL"] +'case/case_system_variable.html')



@case.route('/history/', methods=['GET'])
@login_required
def case_history():
    return render_template(current_app.config["THEME_URL"] +'case/history.html')


@case.route('/tools/', methods=['GET'])
@login_required
def tools():
    case =None
    try:
        get_case = request.urlopen('{0}/common/tools'.format(global_url))
        # get_case = request.urlopen('http://127.0.0.1:5000/api/mock/case/{0}'.format(case_id))
        result = get_case.read()

    except:
        current_app.logger.exception(traceback.format_exc())
        pass
    else:
        json_result = json.loads(result)
        print(json_result)
        if "code" in json_result and "data" in json_result:
            if json_result["code"] == 0:
                if json_result["data"] is not None:
                    case = json_result["data"]

    return render_template(current_app.config["THEME_URL"] +'case/tools.html',tools = case)




