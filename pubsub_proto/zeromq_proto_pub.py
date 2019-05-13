#!python3

import cv2
import numpy as np
import os
import sys
import time
import zmq

sys.path.append(os.path.join(os.path.dirname('__file__'), '..'))

from proto import image_zmq_pb2


input_video_path = '../data/test_video.mp4'
cap = cv2.VideoCapture(input_video_path)
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

msg_out = image_zmq_pb2.Image()

print("All ready, starting to spam:\n")

# wait for subscribers
time.sleep(1)

cost_time = []
while True:
    ret, img = cap.read()
    if not ret:
        break

    start_t = time.time()

    msg_out.msg_id += 1
    msg_out.millis = int(time.time() * 1000 * 1000)
    msg_out.height = img.shape[0]
    msg_out.width = img.shape[1]
    msg_out.channel = img.shape[2]
    msg_out.data = np.ndarray.tobytes(img)
    msg = msg_out.SerializeToString()

    serialize_cost_t = time.time() - start_t
    print('serialize_cost_t', serialize_cost_t)
    cost_time.append(serialize_cost_t)

    s.send_multipart((topic.encode('utf-8'), msg))

    time.sleep(t_sleep_ms/1000)

msg_out.msg_id = 0
msg_out.millis = 0

msg = msg_out.SerializeToString()   # bytes
s.send_multipart((topic.encode('utf-8'), msg))

print('\naverage serialize cost time [sec]:', format(np.mean(cost_time), '.3f'))

print("Done.\n")
