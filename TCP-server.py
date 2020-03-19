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
glnr = "HeShuaiyong"

tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 创建TCP服务器套接字
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)  # 套接字与地址绑定
tcpSerSock.listen(10)  # 监听连接，同时连接请求的最大数目

while True:
    try:
        print("等待客户端的连接...")
        tcpCliSock, addr = tcpSerSock.accept()  # 等待接收客户端连接请求
        print("连接成功：", addr)
        while True:
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            TCP = open("TCP.log", 'a')
            data = tcpCliSock.recv(BS)  # 连续接收指定字节的数据，接收到的是字节>数组
            if glnr.encode('utf8') in data:
                dd = "./dingding.py {}".format(data.decode(encoding='UTF-8'), 'ignore')
                p = subprocess.call(dd, shell=True)
                time.sleep(4)
                if p == 0:
                    print("发送成功：{}".format(date) + '\n' + data.decode(encoding='UTF-8') + '\n')
                    TCP.write("发送成功：{}".format(date) + " " + data.decode(encoding='UTF-8') + '\n')
                else:
                    print("发送失败：{}".format(date) + '\n' + data.decode(encoding='UTF-8') + '\n')
                    TCP.write("发送失败：{}".format(date) + " " + data.decode(encoding='UTF-8') + '\n')
            else:
                print("忽略发送：{}".format(date) + '\n' + data.decode(encoding='UTF-8') + '\n')
                TCP.write("忽略发送：{}".format(date) + " " + data.decode(encoding='UTF-8') + '\n')
            if not data:  # 如果数据空白，则表示客户端退出，所以退出接收
                break
            msg = "YES"
            tcpCliSock.send(msg.encode('utf8'))  # 向客户端状态数据
            TCP.close()
        date = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        TCPTS = open("TCPTS.log", 'a')
        tscl = "./weixin.py HeShuaiyong 服务断开，请重新连接 \"当前时间：{}\"".format(date)
        d = subprocess.call(tscl, shell=True)
        if d == 0:
            print("发送成功：HeShuaiyong 服务断开，请重新连接 当前时间：{}".format(date) + '\n')
            TCPTS.write("发送成功：HeShuaiyong 服务断开，请重新连接 当前时间：{}".format(date) + '\n')
        else:
            print("发送失败：HeShuaiyong 服务断开，请重新连接 当前时间：{}".format(date) + '\n')
            TCPTS.write("发送失败：HeShuaiyong 服务断开，请重新连接 当前时间：{}".format(date) + '\n')
        TCPTS.close()
        tcpCliSock.close()  # 关闭与客户端的连接
    except KeyboardInterrupt:
        print('\n检测到异常，即将退出')
        break
tcpSerSock.close()  # 关闭服务器socket
