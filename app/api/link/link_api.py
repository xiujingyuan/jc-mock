import codecs
import datetime
import os
import random
import traceback

from flask import Flask, jsonify, request, current_app, json
from urllib import request as url_request
import requests
from flask_login import current_user

from app.api.jc_mock import mock
from app import db, csrf
from app.api.link import api_link
from app.common.components.decorators import serialize
from app.models.AnonymousUserModel import AnonymousUser
from app.models.LinkModel import Link
from app.models.UserLinkDb import UserLink


@api_link.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Link API!'


@api_link.route('/click', methods=["POST"])
def update_link():
    ret = {
        "code": 1,
        "msg": "update error"
    }
    req = request.json
    # print(dir(current_user))
    if not current_user.is_anonymous:
        if "link_id" in req:
            link_id = req["link_id"]
            link_obj = UserLink.query.filter_by(user_link_link_id=link_id, user_link_user_id=current_user.id).all()
            if link_obj:
                link_obj[0].user_link_link_count += 1
                db.session.add(link_obj[0])

                ret["code"] = 0
                ret["msg"] = "success"
            else:
                new_link_item = UserLink(user_link_link_id=link_id, user_link_user_id=current_user.id,
                                         user_link_link_count=1)
                db.session.add(new_link_item)
                ret["code"] = 0
                ret["msg"] = "success"
            db.session.flush()
    else:
        ret = {
            "code": 0,
            "msg": "AnonymousUser"
        }
    return jsonify(ret)


@api_link.route('/common_click', methods=["GET"])
def get_common_links_by_user():
    ret = {"code": 1,
           "msg": "error",
           "data": []}
    if not current_user.is_anonymous:
        common_links = UserLink.query.filter_by(user_link_user_id=current_user.id).\
            order_by(UserLink.user_link_link_count.desc()).limit(10)
        for common_link in common_links:
            ret["data"].append(serialize(Link.query.filter_by(link_id=common_link.user_link_link_id).one()))
        ret["code"] = 0
        ret["msg"] = "success"
    return jsonify(ret)
