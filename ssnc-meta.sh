#!/bin/bash

# Usage:
# ./ssnc-meta.sh test/meta.xml
# ./ssnc-meta.sh -f "%artist, %title, %album" -e "\n\n\n\n" test/meta.xml

# echo $1

# hostname=$(hostname)
# whoami=$(whoami)

# printf "Surname: %s\nName: %s\n" "$hostname" "$whoami"

metadata_file="$1"

METADATA_IN_PROGRESS=false

while read -r line
do
  # echo $line | awk -F'[<>]' '/type/{ print $3 }' | read type1
  read type_hex code_hex length <<< $(echo $line | awk -F '[<>]' '/type/{ print $3, " ", $7, " ", $11 }')

  # echo "type_hex: $(echo 0x$type_hex | xxd -r)"
  # echo "code_hex: $(echo 0x$code_hex | xxd -r)"
  # echo "length: $length"

  type1=$(echo 0x$type_hex | xxd -r)
  code=$(echo 0x$code_hex | xxd -r)

  # echo "type: $type"
  # echo "code: $code"
  # echo "length: $length"

  # if [ -z "$type_hex" ]

  if [ $type1 != "" ] && [ $code != "" ] && [ $length != "" ]
  then
    if (( $length > 0 ))
    then
      read data_header > /dev/null
      # echo $data_header
      read data_tag

      # printf ", data: \""

      if [ $code != 'PICT' ]
      then
        payload=$(echo $data_tag | awk -F '<' '{ print $1 }' | base64 --decode)
      fi

      # echo '"'
    else
      echo '(no data - length is 0)'
    fi

    # echo $payload

    case $code in
    'asal')
      echo "Album: $payload"
      ;;
    'asar')
      echo "Artist: $payload"
      ;;
    'ascm')
      echo "Comment: $payload"
      ;;
    'asgm')
      echo "Genre: $payload"
      ;;
    'minm')
      echo "Title: $payload"
      ;;
    *)
      # echo 'Unknown code'
      if [ $type1 == 'ssnc' ]
      then
        echo "type: $type1, code: $code, payload: $payload"
      fi
      ;;
    esac

  else
    echo "ERROR: Tag expected. Got \"$line\" instead."
  fi
done < "$metadata_file"

# while [  $COUNTER -lt 10 ]; do
#   echo The counter is $COUNTER
#   let COUNTER=COUNTER+1
# done
