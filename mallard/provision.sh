#!/bin/bash
set -x

if test -f "Mallard-main.zip"; then
    echo Unzipping Mallard
    unzip -o Mallard-main.zip
fi

date > INSTALL-date.txt

exit 1
