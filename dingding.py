#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
import sys
import json
import time
import urllib3
import importlib

importlib.reload(sys)
urllib3.disable_warnings()


def sendmessage(user, subject, content, token):
    n = 0
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=%s" % token
    data = {
        "msgtype": "text",
        "text": {
            "content": subject + '\n' + content
        },
        "at": {
            "atMobiles": [
                user
            ],
            "isAtAll": False
        }
    }
    # headers = {'Content-Type': 'application/json; charset=UTF-8'}
    headers = {'Content-Type': 'application/json'}
    x = requests.post(url=webhook, data=json.dumps(data), headers=headers)
    print(x.text)  # 请求返回内容
    print(x.status_code)  # 请求返回状态
    while x.json()['errcode'] != 0 and n < 4:
        n += 1
        x = requests.post(url=webhook, data=json.dumps(data), headers=headers)
    if os.path.exists("/tmp/zabbix_dingding.log"):
        f = open("/tmp/zabbix_dingding.log", "a+")
    else:
        f = open("/tmp/zabbix_dingding.log", "w+")
    if x.json()["errcode"] != 0:
        f.write("--" * 30 + '\n')
        f.write(str(x.json()))
        f.write("发送失败" + "    " + str(time) + "    " + str(user) + '\n' + str(subject) + '\n' + str(content) + '\n')
        f.close()
    return x.json()


def zabbixtj(subject):
    if "故障" in subject:
        lines = [i for i in open('./jilu.txt', 'r', encoding="utf-8") if subject not in i]
        f = open('./jilu.txt', 'w', encoding="utf-8")
        f.writelines(lines)
        f.write(subject + '\n')
        f.close()
    elif "已恢复" in subject:
        lines = [i for i in open('./jilu.txt', 'r', encoding="utf-8") if subject.replace("已恢复", "故障") not in i]
        f = open('./jilu.txt', 'w', encoding="utf-8")
        f.writelines(lines)
        f.close()


if __name__ == '__main__':
    user = sys.argv[1]                                                                # zabbix传过来的第一个参数
    subject = str(sys.argv[2])                                                        # zabbix传过来的第二个参数
    content = str(sys.argv[3])                                                        # zabbix传过来的第三个参数

    token = "061100c63a81fd4e66ab728e44f8c11804587e1abaaff0e63e14312ee6eb95d3"
    # token = "580b926491d710c552ed3eb008243cf12650ecb34af45fc2607a8979329873a4"
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    dingding = sendmessage(user, subject, content, token)
    zabbixtj(subject)
