#!/bin/bash

cd pubsub
python3 zeromq_sub.py & python3 zeromq_pub.py
