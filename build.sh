#!/bin/bash
# Simple script to build KAS into an executable for Debian Linux using pyinstaller

base=`dirname $0`
cd "$base"

name=`basename $0 .sh`

if [ ! -d ${base}/deploy ]; then
  mkdir ./deploy
fi

pyinstaller --onefile --windowed --distpath deploy --workpath out -y --clean -p src -p lib src/kas.py

cd deploy
if [ -e kas.zip ]; then
  rm -f kas.zip
fi
zip kas.zip kas

