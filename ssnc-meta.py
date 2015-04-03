#!/usr/bin/python

import argparse, re #, base64

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', required=True)
parser.add_argument('-e', '--endscreen')
parser.add_argument('fifo')
args = parser.parse_args()

# print args.format
# print args.endscreen
# print args.fifo

metadata_in_progress=False
data_mode=False

with open(args.fifo) as f:
  for line in f:
    tag_match = re.match('<type>(\w+)<\/type><code>(\w+)<\/code><length>(\d+)<\/length>', line, flags=re.IGNORECASE)
    data_match = re.match('([a-zA-Z0-9]+={0,2})<\/data>', line, flags=re.IGNORECASE)
    if tag_match:
      # This line is a tag
      # Decompose data from tag
      type_hex, code_hex, length = tag_match.groups()
      type = type_hex.decode('hex')
      code = code_hex.decode('hex')
      # print "type:%s code:%s length:%s" % (type, code, length)



      if code == 'mdst':
        # Metadata start
        metadata_in_progress=True
      elif code == 'pend':
        # Play stream end
        # Do end screen
        print 'end'

      # if length > 0:
        # data_mode=True
        # next(f)
        # print f.readline()

      # if code == 'asal':
      #   album = payload
      # elif code == 'asar':
      #   artist = payload
      # elif code == 'ascm':
      #   comment = payload
      # elif code == 'asgm':
      #   genre = payload
      # elif code == 'minm':
      #   title = payload
      # else:
      #   print 'Unknown code'

      if type == 'ssnc':
        # print "type:%s code:%s payload:%s" % (type, code, payload)
        print "type:%s code:%s" % (type, code)

      else:
        # Metadata start
        metadata_in_progress=False

    elif '<data encoding="base64">' in line:
      # This line is a data start tag
      continue
    elif data_match:
      # This line is data and a data end tag
      data = data_match.groups()[0].decode('base64')
      print data
    else:
      print "Tag expected - got %s instead" % line
