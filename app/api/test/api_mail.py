#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/07/31
 @file: api_mail.py
 @site:
 @email:
"""
import codecs

from flask import current_app
from flask import jsonify
from flask_mail import Message

from app import mail
from app.api.test import test
from app.models.AssumptEmailDb import AssumptEmail
from environment.common.config import Config


@test.route("/mail", methods=['GET'])
def mail_test_fuc():
    msg = Message('test subject', sender=Config.ADMINS[0], recipients=Config.ADMINS)
    msg.body = 'text body'
    msg.html = '<b>HTML</b> body'
    mail.send(msg)

    return jsonify({"code": 1,
                    "message": "success"
                    })


@test.route("/mail/receive", methods=['GET'])
def mail_receive_fuc():

    return jsonify({"code": 1,
                    "message": "success"
                    })


@test.route("/change_content/<int:email_id>", methods=["GET"])
def change_content(email_id):
    email = AssumptEmail.query.filter(AssumptEmail.email_id == email_id).first()
    ret = {
        "code": 1,
        "msg": "not found"
    }
    if email is not None:
        import re, os
        get_content = email.email_content
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*', re.I)
        content = re_script.sub("", get_content)
        ret["msg"] = content
        email_file = os.path.join(os.path.dirname(current_app.instance_path),
                                  "app/static/email/{0}.html".format(email_id))
        print(email_file)
        print(type(content))
        content = content.replace('<link rel="stylesheet" type="text/css" href="/css_'
                                  'dist/report/preview-7e8ad2c4a8.css" />', "")

        content = content.replace('> >>', "")

        with codecs.open(email_file, "w+") as save_email_file:
            save_email_file.write(content)
        ret["code"] = 0
    return jsonify(ret)
