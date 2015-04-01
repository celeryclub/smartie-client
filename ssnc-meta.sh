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

  if [ $code == 'mdst' ]
  then
    METADATA_IN_PROGRESS=true
  fi

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
      if [ $code != 'PICT' ]
      then
        payload=$(echo $data_tag | awk -F '</' '{ print $1 }' | base64 --decode)
      fi
    else
      :
      # echo '(no data - length is 0)'
    fi

    # echo $payload

    case $code in
    'asal')
      # echo "Album: $payload"
      ALBUM=$payload
      ;;
    'asar')
      # echo "Artist: $payload"
      ARTIST=$payload
      ;;
    'ascm')
      # echo "Comment: $payload"
      COMMENT=$payload
      ;;
    'asgm')
      # echo "Genre: $payload"
      GENRE=$payload
      ;;
    'minm')
      # echo "Title: $payload"
      TITLE=$payload
      ;;
    *)
      # echo 'Unknown code'
      if [ $type1 == 'ssnc' ]
      then
        :
        # echo "type: $type1, code: $code, payload: $payload"
      fi
      ;;
    esac

    if [ $code == 'mden' ]
    then
      METADATA_IN_PROGRESS=false
      echo "$ALBUM, $ARTIST, $COMMENT, $GENRE, $TITLE"
    fi

  else
    echo "ERROR: Tag expected. Got \"$line\" instead."
  fi
done < "$metadata_file"
