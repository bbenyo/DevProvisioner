#!/bin/bash
set -x

if test -f "exiftool-master.zip"; then
    echo Unzipping exiftool-master
    unzip exiftool-master.zip .
fi

date > INSTALL-date.txt

exit 1
