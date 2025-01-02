#!/bin/bash
set -x

if test -f "wfuzz-master.zip"; then
    echo Unzipping wfuzz
    unzip -o wfuzz-master.zip
fi

date > INSTALL-date.txt

exit 1
