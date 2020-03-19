#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
import pika
import serial
import serial.tools.list_ports
from pika import channel

MQ_CONFIG = {
    "host": "182.92.192.102",
    "port": 5672,
    "vhost": "/",
    "user": "root",
    "passwd": "Az32729842+-.",
}


def open_port(portx, bps, timeout):
    ret = False
    try:
        ser = serial.Serial(portx, bps, timeout=timeout)
        if ser.isOpen():
            ret = True
            print("open succeed -", ser.name)
        else:
            print("open failed -", ser.name)
    except Exception:
        print("---异常---")
    return ser, ret


def open_scoket():
    zhiling = ['ATE0', 'AT+CIPSHUT', 'AT+CGCLASS=\"B\"', 'AT+CIPCSGP=1,\"CMNET\"', 'AT+CGATT=1', 'AT+CIPMODE=1',
               'AT+CSTT=\"CMNET\"', 'AT+CIICR', 'AT+CIFSR', 'AT+CIPSHUT', 'AT+CIPSTART=\"TCP\",\"39.105.176.17\",\"3000\"']
    for index in zhiling:
        ser.write((index + '\r\n').encode('utf8'))
        print(str(index))
        data = ser.read(1)
        sleep(0.1)
        data = (data + ser.read(ser.inWaiting())).decode('utf-8')
        if "OK" in data:
            print("OK")
        if "YES" in data:
            print(data)
            break
        else:
            sleep(5)
    connect_mq()


def connect_mq():
    credentials = pika.PlainCredentials(MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
    parameters = pika.ConnectionParameters(MQ_CONFIG.get("host"), MQ_CONFIG.get("port"),
                                           MQ_CONFIG.get("vhost"), credentials)
    connection = pika.BlockingConnection(parameters)
    # 声明管道
    channel = connection.channel()
    # 如果确定已经声明了，可以不声明。但是你不知道那个机器先运行，所以要声明两次。
    result = channel.queue_declare('zabbix', durable=True, exclusive=False)
    channel.exchange_declare(exchange='zabbix', durable=True, exchange_type='direct')
    channel.queue_bind(exchange='zabbix', queue=result.method.queue, routing_key='zabbix')
    # channel.basic_consume(callback,queue=zabbix, auto_ack=False)
    ser.write(("ATE0" + '\r\n').encode('utf8'))
    data = ser.read(1)
    sleep(0.1)
    data = (data + ser.read(ser.inWaiting())).decode('utf-8')
    if "YES" in data:
        try:
            print("=====================链接服务器成功=====================")
            channel.basic_consume(result.method.queue, callback, auto_ack=False)
            channel.start_consuming()
        except Exception:
            channel.close()
            open_scoket()
        else:
            channel.close()
            open_scoket()


def callback(ch, method, properties, body):
    ser.write((body.decode('utf8') + '\r\n').encode('utf8'))
    data = ser.read(1)
    sleep(0.1)
    data = (data + ser.read(ser.inWaiting())).decode('utf-8')
    if "YES" in data:
        sleep(1)
    else:
        channel.close()
        open_scoket()
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    try:
        ser, ret = open_port("COM1", 9600, None)
        if ret == True:
            open_scoket()
    except EnvironmentError as err:
        print(err)
        ser.close()
    except KeyboardInterrupt:
        ser.close()
