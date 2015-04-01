#!/bin/bash

# Usage:
# ./clock.sh ticker.fifo
# tail -f ticker.fifo

ticker_file="$1"

# echo $1

rm -f $ticker_file
mkfifo $ticker_file

while true
do
  echo $(date +%I:%M:%S) | cat > $ticker_file
  sleep 1
done
