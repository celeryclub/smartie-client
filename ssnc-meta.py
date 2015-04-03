#!/usr/bin/python

import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', required=True)
parser.add_argument('-e', '--endscreen')
parser.add_argument('fifo')
args = parser.parse_args()

metadata = {}
reading_header = False
reading_data = False
next_data_bucket = None

with open(args.fifo) as f:
  for line in f:
    # print reading_header
    if reading_header:
      # This line is a data header
      if '<data encoding="base64">' in line:
        reading_header = False
        reading_data = True
        continue
      else:
        print 'Error: Expected base64 header, got %s' % line
    elif reading_data and next_data_bucket:
      # This line is data
      datum_match = re.match('([a-zA-Z0-9]+={0,2})<\/data>', line, flags=re.IGNORECASE)
      if datum_match:
        metadata[next_data_bucket] = datum_match.groups()[0].decode('base64')
        reading_data = False
        continue
      else:
        print 'Error: Expected data, got %s' % line
    else:
      tag_match = re.match('<type>(\w+)<\/type><code>(\w+)<\/code><length>(\d+)<\/length>', line, flags=re.IGNORECASE)
      if tag_match:
        # This line is a tag
        type_hex, code_hex, length_string = tag_match.groups()
        type = type_hex.decode('hex')
        code = code_hex.decode('hex')
        length = int(length_string)

        # if code == 'mdst'
        # elif code == 'mden'
        if code == 'mden':
          print metadata
          metadata = {}

        if length > 0:
          next_data_bucket = code
          reading_header = True
          continue
        # elif length 0
      else:
        # This line is malformed
        print 'Error: Expected tag, got %s' % line
