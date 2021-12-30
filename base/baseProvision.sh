#!/bin/bash
set -x

echo Hello!

## Base provisioner
# Base tools
sudo apt-get -y install openjdk-8-jdk-headless
sudo apt-get -y install python3.8
sudo apt-get -y install python

sudo apt-get -y install python3-pip
sudo apt-get -y install python-pip

sudo apt-get -y install bzip2

# Nmap
sudo apt-get -y install nmap

# John
sudo apt-get -y install wordlist
sudo apt-get -y install john

python3 -m pip install --upgrade pip
python -m pip install --upgrade pip

python3 -m pip install --upgrade setuptools
python -m pip3 install --upgrade setuptools

sudo apt-get -y install ruby

date > VERSION-date.txt

exit 1
