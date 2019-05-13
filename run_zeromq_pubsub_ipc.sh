#!/bin/bash

cd pubsub_ipc
python3 zeromq_sub.py & python3 zeromq_pub.py
