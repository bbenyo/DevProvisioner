#!/bin/bash
set -x

if test -d "scapy"; then
    mv scapy scapy-master
fi

pushd scapy-master
sudo python3 setup.py install

python3 -m pip install ipython
python3 -m pip install matplotlib
python3 -m pip install pyx
python3 -m pip install cryptography
python3 -m pip install sphinx
python3 -m pip install sphinx_rtd_theme
python3 -m pip install tox

pushd doc/scapy
make html

popd
popd

date > INSTALL-date.txt

exit 1
