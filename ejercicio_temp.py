#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 20:37:34 2023

@author: david
"""

from paho.mqtt.client import Client
import traceback
import sys
import time 
import random
import numpy as np

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    try:
        n =  float(msg.payload)
        topics = ["t1", "t2"]
        for topic in topics:
            if msg.topic == 'temperature/' + topic:
                if userdata['maximo_'  + topic] < n:
                    userdata['maximo_' + topic] = n
                if userdata['minimo_'  + topic] > n:
                    userdata['minimo_' + topic] = n
                if userdata['maximo'] < n:
                    userdata['maximo'] = n
                if userdata['minimo'] > n:
                    userdata['minimo'] = n
                userdata['total_' + topic] += n
                userdata['total'] += n
                userdata['numero_datos_' + topic] += 1
                userdata['numero_datos'] += 1
    except ValueError:
        pass
    except Exception as e:
        raise e

def media (suma_total, num):
    return suma_total/num
def main(broker):
    keys = ["_t1", "_t2", ""]
    userdata = dict()
    for key in keys:
        userdata["maximo" + key]       = 0
        userdata["minimo" + key]       = np.inf
        userdata["total" + key]        = 0
        userdata["numero_datos" + key] = 0

    client = Client(userdata=userdata)
    client.on_message = on_message

    print(f'Connecting on channels numbers on {broker}')
    client.connect(broker)
    
    client.subscribe('temperature/#')

    client.loop_start()
    t_0 = time.time()

    while True:
        if (time.time()-t_0) > 6: 
            media_t1 = userdata['total_t1'] / userdata['numero_datos_t1']
            media_t2 = userdata['total_t2'] / userdata['numero_datos_t2']
            media    = str(userdata['total'] / userdata['numero_datos'])
            for key in keys:
                print('/clients/maximo' + key
                               , f'{userdata["maximo" + key]}')
                print('/clients/minimo' + key
                               , f'{userdata["minimo" + key]}')
                print('/clients/media' + key
                               , f'{media + key}')
            time.sleep(random.random())
            t_0 = time.time()

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} broker")
    broker = sys.argv[1]
    main(broker)