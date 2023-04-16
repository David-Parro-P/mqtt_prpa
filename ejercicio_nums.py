#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 22:04:21 2023

@author: david
"""

from paho.mqtt.client import Client
import sys

def on_message(client, userdata, msg):
    print("Mensaje:", msg.topic, "El numero es: ", msg.payload)
    value = float(msg.payload.decode("utf-8"))
    messages.append(value)
    if value.is_integer():
        if value%2 == 0:
            print("Par")
        else:
            print("Impar")
    else:
        print("Real")
    
def main(broker):
    client = Client()
    client.enable_logger()
    client.on_message = on_message
    client.connect("simba.fdi.ucm.es")
    client.subscribe('numbers/#')
    client.loop_forever()

if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    messages = []
    main(hostname)
