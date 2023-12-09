#!/bin/bash
set -x

if test -f "binwalk-master.zip"; then
    echo Unzipping binwalk
    unzip -o binwalk-master.zip
fi

if test -d "binwalk"; then
    mv binwalk binwalk-master
fi

pushd binwalk-master
# sudo ./deps.sh
sudo python3 setup.py install
popd

date > INSTALL-date.txt

exit 1
