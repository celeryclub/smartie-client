#!/bin/bash

# Usage:
# ./clock.sh -f "%I:%M %p" ticker.fifo
# tail -f ticker.fifo

while [[ $# > 1 ]]
do
  key="$1"

  case $key in
  -f)
    FORMAT="$2"
    shift
    ;;
  *)
    # unknown option
    ;;
  esac
  shift
done

TICKER_FIFO="$1"

rm -f $TICKER_FIFO
mkfifo $TICKER_FIFO

while true
do
  echo $(date +"$FORMAT") | cat > $TICKER_FIFO
  sleep 1
done
