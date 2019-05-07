#!/bin/bash

wget https://github.com/protocolbuffers/protobuf/releases/download/v3.7.1/protoc-3.7.1-linux-x86_64.zip
unzip protoc-3.7.1-linux-x86_64.zip -d protoc3
sudo mv protoc3/bin/* /usr/local/bin/
sudo mv protoc3/include/* /usr/local/include/
echo 'export LD_LIBRARY_PATH=/usr/local/bin:${LD_LIBRARY_PATH}' >> ~/.bashrc
source ~/.bashrc
protoc --version

git clone -b 3.7.x https://github.com/protocolbuffers/protobuf
cd protobuf/python/
sudo python3 setup.py build
sudo python3 setup.py test
sudo python3 setup.py install

