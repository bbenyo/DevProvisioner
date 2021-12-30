#!/bin/bash

if test -f "boofuzz-master.zip"; then
    echo Unzipping boofuzz-master
    unzip boofuzz-master.zip .
fi

popd boofuzz-master

pip3 install boofuzz

exit 1
