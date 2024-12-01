#!/bin/bash
set -x

if test -f "PayloadsAllTheThings-master.zip"; then
    echo Unzipping Payloads
    unzip -o PayloadsAllTheThings-master.zip
fi

date > INSTALL-date.txt

exit 1
