#!/bin/bash
set -x

sudo python3 setup.py install

pushd doc/scapy
make html

popd

exit 1
