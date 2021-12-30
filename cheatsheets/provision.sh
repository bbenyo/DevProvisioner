#!/bin/bash

if test -f "cheatsheets.zip"; then
    unzip -o cheatsheets.zip
    rm cheatsheets.zip
fi

date > INSTALLED-date.txt

exit 1
