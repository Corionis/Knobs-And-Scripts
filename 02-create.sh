#!/bin/bash

base=`dirname $0`
cd "$base"
base=`pwd`

name=`basename $0 .sh`

export PYTHONPATH=${base}/lib

echo "${name}: library $PYTHONPATH"
echo ''

cd src

# Use this line instead to test prompting for the access token
python3 kas.py create --github --private --url https://github.com --name JackFrost --repo JackHome

