#!python3

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import struct
import sys
import time
import zmq

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

print("All ready, waiting to receive")

cost_time_mean = []
while True:
    c = s.recv_multipart()
    topic, byte_send_time, byte_rows, byte_cols, byte_mat_type, data = c

    # Convert byte to integer
    rows = struct.unpack('q', byte_rows)[0]
    cols = struct.unpack('q', byte_cols)[0]
    mat_type = struct.unpack('q', byte_mat_type)[0]
    send_time = struct.unpack('q', byte_send_time)[0]

    if send_time == 0 and rows == 0:
        break

    curr_time = int(time.time() * 1000 * 1000)
    diff_time = (curr_time - send_time) / 1000 / 1000
    print("diff: {}".format(diff_time))

    img_np = np.frombuffer(data, dtype=np.uint8).reshape((rows,cols,3));

    cost_time_mean.append(diff_time)

    cv2.imshow('deserialized_video', img_np)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('\naverage zmq communication diff [sec]:', format(np.mean(cost_time_mean), '.3f'))
cost_time_mean.clear()
cv2.destroyAllWindows()

print("Done.\n")
