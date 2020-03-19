#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pika
import importlib
import sys
importlib.reload(sys)


credentials = pika.PlainCredentials('admin', 'Az32729842+-.')  # mq用户名和密码
# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
connection = pika.BlockingConnection(pika.ConnectionParameters(host='182.92.192.102', port=5672, virtual_host='/', credentials=credentials))
channel = connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建
result = channel.queue_declare('zabbix', durable=True, exclusive=False)
channel.exchange_declare(exchange='zabbix', durable=True, exchange_type='direct')

# message = str(sys.argv[1] + ' ' + sys.argv[2]  + ' ' + sys.argv[3])
message = str(sys.argv[1])
# 向队列插入数值 routing_key是队列名
channel.basic_publish(exchange='zabbix', routing_key='zabbix', body=message, properties=pika.BasicProperties(delivery_mode=2))
print(message)
connection.close()
