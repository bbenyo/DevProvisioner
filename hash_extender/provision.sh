#!/bin/bash
set -x

if test -f "hash_extender-master.zip"; then
    echo Unzipping hash_extender
    unzip -o hash_extender-master.zip
fi

pushd hash_extender-master
make
popd

date > INSTALL-date.txt

exit 1
