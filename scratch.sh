#!/bin/bash

# echo "\"$tst\""
# tst='YES'
# echo "\"$tst\""
# tst='NO'
# echo "\"$tst\""

while [[ $# > 1 ]]
do
key="$1"

case $key in
  -e)
  EXTENSION="$2"
  shift
  ;;
  -s)
  SEARCHPATH="$2"
  shift
  ;;
  -l)
  LIBPATH="$2"
  shift
  ;;
  --default)
  DEFAULT=YES
  shift
  ;;
  *)
  # unknown option
  ;;
esac
shift
done

echo FILE EXTENSION  = "${EXTENSION}"
echo SEARCH PATH     = "${SEARCHPATH}"
echo LIBRARY PATH    = "${LIBPATH}"

if [[ -n $1 ]]; then
  echo "Non-opt/last argument:"
  echo $1
fi
