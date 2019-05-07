#!/bin/bash

protoc --python_out=./ ./proto/image.proto
protoc --python_out=./ ./proto/video.proto
