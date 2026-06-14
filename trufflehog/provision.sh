#!/bin/bash
set -x

go install
./scripts/install.sh

export PATH=$PATH:$PWD/scripts/bin


exit 1
