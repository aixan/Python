#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import time
import importlib
import sys
importlib.reload(sys)

print("=====================TCP客户端=====================")
HOST = '127.0.0.1'  # 服务器ip地址，等价于localhost
PORT = 3000  # 通信端口号
BUFSIZ = 1024  # 接收数据缓冲大小
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建客户端套接字1
tcpCliSock.connect(ADDR)  # 发起TCP连接
while True:
    data = input('请输入：')  # 接收用户输入
    if not data:  # 如果用户输入为空，直接回车就会发送""，""就是代表false
        break
    tcpCliSock.send(bytes(data, 'utf-8'))  # 客户端发送消息
    # data = tcpCliSock.recv(BUFSIZ)  #接收回应消息，接收到的是字节数组
    # if not data:  #如果接收服务器信息失败，或没有消息回应
    # break
    print(data)  # 打印回应消息
tcpCliSock.close()  # 关闭客户端socket
