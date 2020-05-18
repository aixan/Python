#!/usr/bin/python3
# -*- coding: utf-8 -*-

from socket import *
import time
import importlib
import subprocess
import sys
importlib.reload(sys)

print("=====================时间戳TCP服务器=====================")
HOST = ''  # 主机号为空白表示可以使用任何可用的地址。
PORT = 3000  # 端口号
BS = 8192  # 接收数据缓冲大小
ADDR = (HOST, PORT)
glnr = "zabbix"

tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 创建TCP服务器套接字
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)  # 套接字与地址绑定
tcpSerSock.listen(128)  # 监听连接，同时连接请求的最大数目

while True:
    try:
        print("服务器启动，等待客户端的连接...")
        tcpCliSock, addr = tcpSerSock.accept()  # 等待接收客户端连接请求
        tcpCliSock.settimeout(100)
        print("连接成功：", addr)
        print("=" * 30)
        while True:
            try:
                data = tcpCliSock.recv(BS)  # 连续接收指定字节的数据，接收到的是字节>数组
                if data:  # 如果数据空白，则表示客户端退出，所以退出接收
                    print("客户端发送的内容：",data.decode('utf-8'))
                    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    if glnr.encode('utf8') in data:
                        dd = "./dingding.py {}".format(data.decode(encoding='UTF-8'), 'ignore')
                        p = subprocess.call(dd, shell=True)
                        if p == 0:
                            time.sleep(4)
                            print("发送成功：{}".format(date))
                        else:
                            time.sleep(4)
                            print("发送失败：{}".format(date))
                    else:
                        print("忽略发送：{}".format(date))
                    msg = "YES"
                    tcpCliSock.send(msg.encode('utf8'))  # 向客户端状态数据
                    print("=" * 30)
                else:
                    break
            except Exception:
                break
        print("断开的客户端", addr)
        date = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        tscl = "./dingding.py HeShuaiyong 服务断开，请重新连接 \"当前时间：{}\"".format(date)
        d = subprocess.call(tscl, shell=True)
        tcpCliSock.close()
    except KeyboardInterrupt:
        print('\n检测到异常，即将退出')
        break
tcpSerSock.close()  # 关闭服务器socket

