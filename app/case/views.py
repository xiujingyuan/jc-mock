import traceback
import urllib
from functools import wraps

from flask import Flask, jsonify,current_app, request
from flask import render_template, json
from flask_login import login_required, current_user
from urllib import request as url_request
from app.base.views import BaseView
from app.case import case
from environment.common.config import Config


class CaseView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):

        return render_template(current_app.config["THEME_URL"] + 'case/cases.html', **self.context)


case.add_url_rule('/case', view_func=CaseView.as_view('case'), methods=["GET", "POST"])


# class CaseItemView(BaseView):
#     decorators = [login_required]
#
#     def dispatch_request(self, case_id):
#         case = {}
#         try:
#             get_case = url_request.urlopen('{0}/case/{1}'.format(global_url, case_id))
#             result = get_case.read()
#         except:
#             current_app.logger.exception(traceback.format_exc())
#             pass
#         else:
#             json_result = json.loads(result)
#             if "code" in json_result and "data" in json_result:
#                 if json_result["code"] == 0:
#                     if json_result["data"] is not None:
#                         case = json_result["data"]
#         prevInfo = case['prevInfo']
#         initInfo = case['initInfo']
#         self.context.update({"case": case})
#         self.context.update({"prevInfo": prevInfo})
#         self.context.update({"initInfo": initInfo})
#         return render_template(current_app.config["THEME_URL"] +'case/case_edit.html', **self.context)
#
#
# case.add_url_rule('/case/<int:case_id>/', view_func=CaseItemView.as_view('case_item'), methods=["GET", "POST"])


class AddCaseView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'case/case_add.html', **self.context)


case.add_url_rule('/add_case', view_func=AddCaseView.as_view('add_case'), methods=["GET"])


class AddCaseNewView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, case_id):
        case = {}
        try:
            get_case = url_request.urlopen('{0}/case/{1}'.format(current_app.config["BACKEND_URL"], case_id))
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
        prevInfo = case['prevInfo']
        initInfo = case['initInfo']

        self.context.update({"case_id": case_id,
                             "prevInfo": prevInfo,
                             "initInfo": initInfo})
        return render_template(current_app.config["THEME_URL"] + 'case/case_edit_new.html', **self.context)


case.add_url_rule('/case/<int:case_id>/', view_func=AddCaseNewView.as_view('add_case_new'), methods=["GET"])


class CaseSystemVariableView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'case/case_system_variable.html', **self.context)


case.add_url_rule('/case_system_variable', view_func=CaseSystemVariableView.as_view('case_system_variable'), methods=["GET"])


class CaseHistoryView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'case/history.html', **self.context)


case.add_url_rule('/history/', view_func=CaseHistoryView.as_view('case_history'), methods=["GET"])


class ToolsView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        case = None
        try:
            get_case = urllib.request.urlopen('{0}/common/tools'.format(current_app.config["BACKEND_URL"]))
            result = get_case.read()

        except:
            current_app.logger.exception(traceback.format_exc())
            pass
        else:
            json_result = json.loads(result)
            # print(json_result)
            if "code" in json_result and "data" in json_result:
                if json_result["code"] == 0:
                    if json_result["data"] is not None:
                        case = json_result["data"]
        self.context.update({"tools": case})
        return render_template(current_app.config["THEME_URL"] + 'case/tools.html', **self.context)


case.add_url_rule('/tools', view_func=ToolsView.as_view('tools'), methods=["GET"])


class ReportView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        return render_template(current_app.config["THEME_URL"] + 'case/reports.html', **self.context)


case.add_url_rule('/report/', view_func=ReportView.as_view('report'), methods=["GET"])


class ReportDetailView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, report_id):
        self.context.update({"report": report_id})
        return render_template(current_app.config["THEME_URL"] + 'case/reportdetail.html', **self.context)


case.add_url_rule('/report/detail/<int:report_id>', view_func=ReportDetailView.as_view('report_create'), methods=["GET"])


class ReportCreateView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        self.context.update({"report": None})
        return render_template(current_app.config["THEME_URL"] + 'case/reportdetail.html', **self.context)


case.add_url_rule('/detail/create', view_func=ReportCreateView.as_view('detail_create'), methods=["GET"])
