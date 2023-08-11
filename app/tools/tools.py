import requests
from pprint import pformat


def send_qiyeweixin(content):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fc8f03cc-f81c-4269-bfda-c976c1d770ff"
    headers = {'content-type': 'application/json'}
    data = {"msgtype": "text",
            "text": {"content": str(pformat(content))}}
    requests.post(url, json=data, headers=headers)


def send_tv(content):
    url = "https://tv-service-alert.kuainiu.chat/alert"
    headers = {'content-type': 'application/json'}
    data = {"botId": "043be9e1-d720-4186-b5aa-debf1ee238d3",
            "message": str(content)}
    requests.post(url, json=data, headers=headers)


if __name__ == "__main__":
    # send_qiyeweixin("test\ntest")
    send_tv("test\ntest")
    # send_qiyeweixin(["11111111111", "111erfdgfefer ferf erf e 2", "erwer wer wef we we w wev wevfwevwevewv3"])
