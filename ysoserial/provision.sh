#!/bin/bash
set -x

if test -f "ysoserial-master.zip"; then
    echo Unzipping ysoserial
    unzip -o ysoserial-master.zip
fi

date > INSTALL-date.txt

exit 1
