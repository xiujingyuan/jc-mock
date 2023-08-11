#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/08/01
 @file: mail_receive.py
 @site:
 @email:
"""

import poplib
import email
import datetime
import time
from email.header import decode_header
import traceback
import sys
import telnetlib
from flask import current_app
from app import mail
from environment.common.config import Config
from flask_mail import Message


STATUS_SUCCESS = "SUCCESS"


def mail_send(subject, content, recipients=["yangxuechao@kuainiugroup.com"], sender="需求发布", cc=[]):
    """
    发送邮件方法
    :param subject:邮件标题
    :param content: 邮件内容
    :param recipients: 接收人
    :param sender: 发送人
    :return:
    """
    current_app.logger.info("开始发送邮件，需求名:{0}".format(subject))
    msg = Message()
    msg.sender = "{0}<{1}>".format(sender, current_app.config["MAIL_USERNAME"])
    msg.recipients = recipients
    msg.subject = subject
    msg.html = content
    if cc:
        msg.cc = cc
    current_app.logger.info("开始发送邮件，邮件发送完成，流水线编号:{0}".format(subject))
    app = current_app._get_current_object()
    with app.app_context():
        mail.send(msg)


class GetAssumptEmail(object):
    # 字符编码转换
    @staticmethod
    def decode_str(str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 解析邮件,获取附件
    @staticmethod
    def get_att(msg_in, str_day_in):
        # import email
        attachment_files = []
        for part in msg_in.walk():
            # 获取附件名称类型
            file_name = part.get_filename()
            # contType = part.get_content_type()
            if file_name:
                h = email.header.Header(file_name)
                # 对附件名称进行解码
                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    # 将附件名称可读化
                    filename = GetAssumptEmail.decode_str(str(filename, dh[0][1]))
                    print(filename)
                    # filename = filename.encode("utf-8")
                # 下载附件
                data = part.get_payload(decode=True)
                # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                att_file = open(str_day_in + '\\' + filename, 'wb')
                attachment_files.append(filename)
                att_file.write(data)  # 保存附件
                att_file.close()
        return attachment_files

    @staticmethod
    def run_ing(email_id):
        # 输入邮件地址, 口令和POP3服务器地址:
        mail_infos = {}
        email_user = Config.COM_MAIL_USERNAME
        # 此处密码是授权码,用于登录第三方邮件客户端
        password = Config.COM_MAIL_PASSWORD
        pop3_server = Config.MAIL_RECEIVE_SERVER
        # 日期赋值
        day = datetime.date.today()
        str_day = str(day).replace('-', '')
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
        try:
            telnetlib.Telnet(pop3_server, 995)
            server = poplib.POP3_SSL(pop3_server, 995, timeout=10)
        except:
            time.sleep(5)
            server = poplib.POP3(pop3_server, 110, timeout=10)
        # server = poplib.POP3(pop3_server, 110, timeout=120)
        # 可以打开或关闭调试信息
        # server.set_debuglevel(1)
        # 打印POP3服务器的欢迎文字:
        current_app.logger.info("getwelcome {0}".format(server.getwelcome().decode('utf-8')))
        # 身份认证:
        server.user(email_user)
        server.pass_(password)
        # 返回邮件数量和占用空间:
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        # mails, octets = server.stat()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        # 倒序遍历邮件
        # for i in range(index, 0, -1):
        # 顺序遍历邮件
        mail_infos["new_email_id"] = email_id
        mail_infos["data"] = []
        current_app.logger.info("mails is : {0}".format(len(mails)))
        for item_index, i in enumerate(range(len(mails), 0, -1)):
            resp, lines, octets = server.retr(i)
            current_app.logger.info("{0} {1} {2} {3}".format(i, item_index, octets, time.ctime(time.time())))
            if item_index == 0:
                mail_infos["new_email_id"] = octets
            if str(octets) == str(email_id):
                break

            mail_item = {"content": lines, "octets": octets}

            mail_infos["data"].append(mail_item)
        server.quit()
        return mail_infos


if __name__ == '__main__':
    # @version : 3.4
    # @Author  : robot_lei
    # @Software: PyCharm Community Edition
    # log_path = 'C:\\fakepath\\log.log'
    # logging.basicConfig(filename=log_path)
    print("starting")
    origin = sys.stdout
    # f = open('log.txt', 'w')
    # sys.stdout = f
    try:
        GetAssumptEmail.run_ing(0)
    except Exception as e:
        s = traceback.format_exc()
        print(s)
        # tra = traceback.print_exc()
    # sys.stdout = origin
    # f.close()
    print("finished")
