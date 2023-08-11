# coding: utf-8

from app import db
from app.common.Serializer import Serializer


class CommonTool(db.Model, Serializer):
    __tablename__ = 'common_tools'

    common_tools_id = db.Column(db.Integer, primary_key=True)
    common_tools_title = db.Column(db.String(500), info='工具名称')
    common_tools_address = db.Column(db.String(2500), info='工具地址')
    common_tools_method = db.Column(db.String(50), info='请求方法')
    common_tools_placeholder = db.Column(db.Text, info='工具demo')
    common_tools_description = db.Column(db.String(1000), info='工具描述')
    common_tools_update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    common_tools_update_user = db.Column(db.String(20))
    common_tools_create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    common_tools_create_user = db.Column(db.String(20), info='工具开发者')
    common_tools_is_int = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否为联调工具')
    common_tools_req_desc = db.Column(db.String(1000), info='请求参数说明')
    common_tools_resp_desc = db.Column(db.String(1000), info='返回值说明')
