#!/bin/bash
set -x

echo Hello!

## Base provisioner
sudo apt-get -y install openjdk-8-jdk-headless
sudo apt-get -y install python3.8
sudo apt-get -y install python

sudo apt-get -y install python3-pip
sudo apt-get -y install python-pip

sudo apt-get -y install nmap

sudo apt-get -y install bzip2

python3 -m pip install --upgrade pip
python -m pip install --upgrade pip

python3 -m pip install --upgrade setuptools
python -m pip3 install --upgrade setuptools

sudo apt-get -y install ruby

date > VERSION-date.txt

exit 1
