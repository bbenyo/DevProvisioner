#!/bin/bash
set -x

if test -f "hash_extender-master.zip"; then
    echo Unzipping hash_extender
    unzip -o hash_extender-master.zip
    mv hash_extender-master hash_extender
fi

pushd hash_extender
make
popd

date > INSTALL-date.txt

exit 1
