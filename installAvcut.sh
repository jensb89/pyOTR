#!/bin/bash

#Script to download and comile avcut (tested un der MacOS 10 ElCapitan)

git clone https://github.com/anyc/avcut.git avcutApp
cd avcutApp 
make
mv avcut ../Bin/avcut
mv profiles/ ../Bin/
cd ..
rm -rf avcutApp