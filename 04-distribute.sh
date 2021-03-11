#!/bin/bash

base=`dirname $0`
cd "$base"
base=`pwd`

name=`basename $0 .sh`

export PYTHONPATH=${base}/lib

echo "${name}: library $PYTHONPATH"
echo ''

cd src

python3 kas.py distribute --repo Clavius

