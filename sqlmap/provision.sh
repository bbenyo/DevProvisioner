#!/bin/bash
set -x

if test -f "sqlmap-master.zip"; then
    echo Unzipping sqlmap
    unzip -o sqlmap-master.zip
fi

date > INSTALL-date.txt

exit 1
