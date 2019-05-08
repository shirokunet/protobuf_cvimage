#!python3

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import sys
import time
import zmq

from proto import image_zmq_pb2

# b"" to get byte-string

# Ports between 49152 & 65535 are "free" ports

# --- constants ---

port = 50403    # choose however you want
topic = "Benchmark"
publisher = "localhost"

# --- Main ---

print("\n --- Welcome to PB_MQ_Benchmark: SUB --- \n")
print("Subscribing to topic '{}' at '{}' on port '{}'\n".format(topic, publisher, port))

print("Starting Socket")

context = zmq.Context()
s = context.socket(zmq.SUB)

print("Connecting")

s.connect("tcp://{}:{}".format(publisher, port))
s.setsockopt_string(zmq.SUBSCRIBE, topic)

msg_in = image_zmq_pb2.Image()

print("All ready, waiting to receive")

cost_time = []
while True:
    c = s.recv_multipart()
    # start_t = time.time()
    topic, msg = c
    msg_in.ParseFromString(msg)
    # print('deserialize_cost_t', time.time() - start_t)

    # extract values
    send_time = msg_in.millis
    msg_id = msg_in.msg_id

    if send_time == 0 and msg_id == 0:
        break

    curr_time = int(time.time() * 1000 * 1000)
    diff_time = (curr_time - send_time) / 1000 / 1000
    print("diff: {}".format(diff_time))

    img_np = np.frombuffer(msg_in.data, np.uint8)
    img_np = img_np.reshape(msg_in.height, msg_in.width, msg_in.channel)

    cost_time.append(diff_time)

    cv2.imshow('deserialized_video', img_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('\naverage zmq communication diff [sec]:', format(np.mean(cost_time), '.3f'))
cost_time.clear()
cv2.destroyAllWindows()

print("Done.\n")
