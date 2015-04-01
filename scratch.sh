#!/bin/bash

# echo "\"$tst\""
# tst='YES'
# echo "\"$tst\""
# tst='NO'
# echo "\"$tst\""

echo FILE EXTENSION  = "${EXTENSION}"
echo SEARCH PATH     = "${SEARCHPATH}"
echo LIBRARY PATH    = "${LIBPATH}"

if [[ -n $1 ]]; then
  echo "Non-opt/last argument:"
  echo $1
fi
