#!python3

import cv2
import numpy as np
import os
import sys
import time
import zmq


input_video_path = '../data/test_video.mp4'
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    sys.exit()

# b"" to get byte-string

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

port = 50403    # choose however you want
topic = "Benchmark"

t_sleep_ms = 33.333

# --- Main ---

print("\n --- Welcome to PB_MQ_Benchmark: PUB --- \n")
print("Publishing to topic '{}' on port {}\n".format(topic, port))

print("Starting Socket")

context = zmq.Context()
s = context.socket(zmq.PUB)

s.bind("tcp://*:{}".format(port))   # publish on local

print("Creating message")

print("All ready, starting to spam:\n")

# wait for subscribers
time.sleep(1)

cost_time_mean = []
while True:
    ret, img = cap.read()
    if not ret:
        break

    start_t = time.time()

    height, width = img.shape[:2]
    print(height, width)
    ndim = img.ndim
    msg = [topic.encode('utf-8'), 
           np.array([int(time.time() * 1000 * 1000)]), \
           np.array([height]), \
           np.array([width]), \
           np.array([ndim]), \
           img.data]

    serialize_cost_t = time.time() - start_t
    print('serialize_cost_t', serialize_cost_t)
    cost_time_mean.append(serialize_cost_t)

    s.send_multipart(msg)

    time.sleep(t_sleep_ms/1000)

msg = [topic.encode('utf-8'), \
       np.array([0]), \
       np.array([0]), \
       np.array([0]), \
       np.array([0]), \
       np.array([0])]
s.send_multipart(msg)

print('\naverage serialize cost time [sec]:', format(np.mean(cost_time_mean), '.3f'))

print("Done.\n")
