#!/bin/bash

cd protobuf/examples/
protoc --python_out=./ ./addressbook.proto
python3 add_person.py ADDRESS_BOOK_FILE
python3 list_people.py ADDRESS_BOOK_FILE
