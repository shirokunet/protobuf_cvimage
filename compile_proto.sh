#!/bin/bash

protoc --python_out=./ ./proto/image.proto
protoc --python_out=./ ./proto/video.proto
protoc --python_out=./ ./proto/image_zmq.proto
