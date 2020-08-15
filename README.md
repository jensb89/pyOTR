# pyOTR

A python tool to decode, cut and rename video files from onlinetvrecorder.com.

## Setup
Fill in the folder dirs in the config_sample.py and rename the file to config.py.

Download the otrdecoder from https://www.onlinetvrecorder.com/v2/software/ and place it in the Bin folder.

Put a binary of avcut in the Bin folder.

To compile avcut in MacOS, ffmpeg must be installed beforehand. E.g. with
```
brew install sdl2 ffmpeg
```
Then the script installAvcut.sh can be called to download the newest avcut software and compile the binary. The script already places the file in the Bin/Mac folder.

To cross compile avcut, e.g. for a Synology NAS armv7 system, follow these instructions: https://github.com/jensb89/avcut/blob/master/HOWTO_Compile_for_Synology_NAS.MD

## Usage
```
usage: pyOtr [-h] [--single-file fileName] [--decode-only] [--cut-only]
             [--save-cutlist] [--cutlist-file cutlistFile]
             [--no-file-rename NO_FILE_RENAME]

Process and decoded otrkey files and cut the decoded video files.

optional arguments:
  -h, --help            show this help message and exit
  --single-file fileName
                        deocde, cut and sort single file
  --decode-only         only decoding, no cut, no sort
  --cut-only            only cutting, cutlist is automatically downloaded
  --save-cutlist        -stores the cutlist used for cutting the video file
  --cutlist-file cutlistFile
                        If this option is used, a manual cutlist file can be
                        used. Otherwise the best cutlist available from
                        cutlist.at will be used instead.
  --no-file-rename      do not try to rename the file with the season and
                        episode information
```

## Tests
[![Build Status](https://travis-ci.com/jensb89/pyOTR.svg?branch=master)](https://travis-ci.com/jensb89/pyOTR)

Run tests from main folder:
python Tests/unitTests.py

Todo: CI Job

