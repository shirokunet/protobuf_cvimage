#!/bin/bash

cd pubsub_proto
python3 zeromq_proto_sub.py & python3 zeromq_proto_pub.py
