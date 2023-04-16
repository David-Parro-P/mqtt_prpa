#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 23:22:00 2023

@author: david
"""

from paho.mqtt.client import Client
import paho.mqtt.publish as publish
import time, sys, math, random

def total():
    for subtopic in subtopics:
        minimum, maximum, average = sats(subtopics[subtopic])
        print(f"Subtopic: {subtopic}, Min: {minimum}, Max: {maximum}, Media: {average}")
    minimum, maximum, average = sats(messages)
    print(f"Recuento , Min: {minimum}, Max: {maximum}, Media: {average}")
    
def sats(values):
    return min(values), max(values), sum(values) / len(values)


def on_message(client, userdata, msg):
    global startTime, runTime, messages
    print("Mensaje:", msg.topic, msg.payload)
    
    if msg.topic == 'numbers':
        value = float(msg.payload.decode("utf-8"))
        messages.append(value)
        if value.is_integer():
            if value%2 == 0:
                client.unsubscribe('numbers/#')
                print("Par")
                startTime = time.time()
                runTime = random.randint(4, 8)  
                client.subscribe('temperature/#')
            else:
                print("Impar")
        else:
            print("Real")

    else:
        subtopic = msg.topic.split("/")[-1]
        value = float(msg.payload.decode("utf-8"))
        if subtopic in subtopics:
            subtopics[subtopic].append(value)
        else:
            subtopics[subtopic] = [value]   
        messages.append(value)
        
        currentTime = time.time()
        if (currentTime - startTime) > runTime:
            total()
            client.unsubscribe('temperature/#')
            client.subscribe('numbers/#')          

def main(broker):
    client = Client()
    client.on_message = on_message
    client.connect(broker)
    client.subscribe('numbers/#')
    client.loop_forever()

if __name__ == '__main__':
    broker = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        broker = sys.argv[1]
    messages = []
    subtopics = {}
    main(broker)
