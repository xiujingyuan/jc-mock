#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import urllib
from flask import render_template, current_app
import json
from flask_login import login_required
from sqlalchemy import and_
from app.base.views import BaseView
from app.common.Serializer import Serializer
from app.int import view_int
from app.models.CommonToolsDb import CommonTool
from app.models.KeyValueDb import KeyValue
from app.models.TapdCaseDetailDb import TapdCaseDetail
from app.models.rbiz.AssetRbizDb import AssetRbiz
from app.int import view_int
from app import db


class IntView(BaseView):
    decorators = [login_required]

    def dispatch_request(self):
        get_env_base_config = KeyValue.query.filter(KeyValue.key == 'env_base_config').first()
        if get_env_base_config:
            get_env_base_config_value = json.loads(get_env_base_config.value)
            self.context.update({'env_base_config': get_env_base_config_value})

        get_program_url_config = KeyValue.query.filter(KeyValue.key == 'program_url_config').first()
        if get_program_url_config:
            get_program_url_config_value = json.loads(get_program_url_config.value)
            self.context.update({'program_url_config': get_program_url_config_value})

        get_all_common = CommonTool.query.filter(CommonTool.common_tools_is_int == 1).all()
        get_all_common_json = Serializer.serialize_list(get_all_common)
        self.context.update({"tools": get_all_common_json})

        return render_template(current_app.config["THEME_URL"] + 'int/int_index.html', **self.context)


view_int.add_url_rule('/', view_func=IntView.as_view('int'), methods=["GET"])
