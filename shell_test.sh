#!/bin/sh
echo "Running..."
output=$(python "download_cutlist.py" "asd" 2>&1) #http://stackoverflow.com/questions/11900828/store-return-value-of-a-python-script-in-a-bash-script
echo "Finished"
echo "$output"
echo "Output <"
echo $? #error code from python script http://stackoverflow.com/questions/285289/exit-codes-in-python