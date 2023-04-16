#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 21:39:19 2023

@author: david
"""

from paho.mqtt.client import Client
from multiprocessing import Process
from time import sleep


def timer(client, msg):
    mensaje = msg.payload.split(", ")
    delay, topic, contenido = mensaje[0], mensaje[1], mensaje[2]
    sleep(float(delay))
    client.publish(topic, contenido)

def on_message(client, data, msg):
    try:
        p = Process(target = timer, args=(client, msg)) 
        p.start()
    except Exception as e:
        print(e)

    
def main(broker):
    data={'status' : 0}
    client = Client(userdata=data)
    client.on_message = on_message
    client.connect(broker)
    client.subscribe("clients/timer")
    client.publish
    client.loop_forever
    
if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)