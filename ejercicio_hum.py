#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 22:41:10 2023

@author: david
"""

from paho.mqtt.client import Client
import sys

MIN = 25  
MAX = 40  

def on_message(client, userdata, msg):
    print(userdata, msg.topic, msg.payload)
    if msg.topic == "temperature/t1":
        temp = float(msg.payload)
        if temp > MIN:
            client.subscribe("humidity")
            userdata['humidity'] = True
        else:
            client.unsubscribe("humidity")
            userdata['humidity'] = False
    elif msg.topic == "humidity":
        humidity = float(msg.payload)
        if humidity > MAX:
            client.unsubscribe("temperature/t1")
            userdata['humidity'] = False

def main(broker):
    data = {'humidity': False}
    client = Client(userdata=data)
    client.on_message = on_message
    client.connect(broker)
    client.subscribe('temperature/t1')
    client.loop_forever()

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)
