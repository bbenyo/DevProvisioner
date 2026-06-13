#!/bin/bash

sudo apt-get install -y python3-venv build-essential
mkdir boofuzz && cd boofuzz
python3.10 -m venv env
source env/bin/activate
pip install -U pip setuptools
pip install boofuzz

exit 1
