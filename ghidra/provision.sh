#!/bin/bash
set -x

if test -f "ghidra-master.zip"; then
    echo Unzipping ghidra
    unzip -o ghidra-master.zip
fi

date > INSTALL-date.txt

exit 1
