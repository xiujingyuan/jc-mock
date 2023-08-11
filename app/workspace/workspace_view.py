#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import urllib
from flask import render_template, current_app
import json
from flask_login import login_required
from sqlalchemy import and_
from app.base.views import BaseView
from app.models.KeyValueDb import KeyValue
from app.models.TapdCaseDetailDb import TapdCaseDetail
from app.models.rbiz.AssetRbizDb import AssetRbiz
from app.workspace import view_workspace
from app import db


class WorkSpaceView(BaseView):
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

        return render_template(current_app.config["THEME_URL"] + 'workspace/workspace_index.html', **self.context)


view_workspace.add_url_rule('/', view_func=WorkSpaceView.as_view('workspace'), methods=["GET"])
