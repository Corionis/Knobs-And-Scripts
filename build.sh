#!/bin/bash
# Simple script to build KAS into an executable for Debian Linux

base=`dirname $0`
cd "$base"

name=`basename $0 .sh`

if [ ! -d ./deploy ]; then
  mkdir ./deploy
fi

pyinstaller --onefile --windowed --distpath deploy --workpath build -y --clean -p src -p lib src/kas.py
