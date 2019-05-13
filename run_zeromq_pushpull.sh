#!/bin/bash

cd pushpull
python3 zeromq_push.py & python3 zeromq_pull.py
