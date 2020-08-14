# pyOTR

A python tool to decode, cut and rename video files from onlinetvrecorder.com.

## Setup
Fill in the folder dirs in the config_sample.py and rename the file to config.py.

On mac to compile avcut:
brew install sdl2 ffmpeg

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
  --no-file-rename NO_FILE_RENAME
                        do not try to rename the file with the season and
                        episode information
```

## Tests
Run tests from main folder:
python Tests/unitTests.py

Todo: CI Job

