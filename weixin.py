#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
import json
import os
import time
import urllib3
import importlib

importlib.reload(sys)
urllib3.disable_warnings()


def gettokenfromserver(corpid, secret):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    data = {
        "corpid": corpid,
        "corpsecret": secret
    }
    r = requests.get(url=url, params=data, verify=False)
    # print(r.json())
    if r.json()['errcode'] != 0:
        return False
    else:
        token = r.json()['access_token']
        file = open('/tmp/zabbix_wechat_config.json', 'w')
        file.write(r.text)
        file.close()
        return token


def sendmessage(user, agentid, subject, content):
    try:
        file = open('/tmp/zabbix_wechat_config.json', 'r')
        token = json.load(file)['access_token']
        file.close()
    except:
        token = gettokenfromserver(corpid, secret)
    n = 0
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
    data = {
        "touser": user,           # 企业号中的用户帐号，在zabbix用户Media中配置，如果配置不正常，将按部门发送。
        # "totag": tagid,         # 企业号中的标签id，群发使用（推荐）
        "toparty": partyid,       # 企业号中的部门id，群发时使用。
        "msgtype": "text",        # 消息类型。
        "agentid": agentid,       # 企业号中的应用id。
        "text": {
            "content": subject + '\n' + content
        },
        "safe": "0"
    }
    r = requests.post(url=url, data=json.dumps(data), verify=False)
    while r.json()['errcode'] != 0 and n < 4:
        n += 1
        token = gettokenfromserver(corpid, secret)
        if token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
            r = requests.post(url=url, data=json.dumps(data), verify=False)
            # print(r.json())
    if os.path.exists("/tmp/zabbix_weixin.log"):
        f = open("/tmp/zabbix_weixin.log", "a+")
    else:
        f = open("/tmp/zabbix_weixin.log", "w+")
    f.write("--" * 30 + '\n')
    if r.json()["errcode"] == 0:
        f.write("发送成功" + "    " + str(time) + "    " + str(user) + '\n' + str(subject) + '\n' + str(content) + '\n')
        f.close()
    else:
        f.write("发送失败" + "    " + str(time) + "    " + str(user) + '\n' + str(subject) + '\n' + str(content) + '\n')
        f.close()
    return r.json()


if __name__ == '__main__':
    user = sys.argv[1]                                                                # zabbix传过来的第一个参数
    subject = str(sys.argv[2])                                                        # zabbix传过来的第二个参数
    content = str(sys.argv[3])                                                        # zabbix传过来的第三个参数

    corpid = "ww9f4c7a1cda6c169e"                                                     # CorpID是企业号的标识
    secret = "fqduom2qV_VC694BaEAv2l9rM9x88vczJ1ej55eZ8Ws"                            # Secret是管理组凭证密钥
    tagid = "1"                                                                       # 通讯录标签ID
    agentid = "1000002"                                                               # 应用ID
    partyid = "1"                                                                     # 部门ID

    time = time.strftime('%Y-%m-%d %H:%M:%S')
    weixin = sendmessage(user, agentid, subject, content)

