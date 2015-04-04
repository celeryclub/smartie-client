#!/usr/bin/python

# Usage:
# python ssnc-meta.py -f '%title\n%artist\n%album\n' test/meta.xml

import argparse, re

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', required=True)
parser.add_argument('-e', '--endscreen')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('fifo')
args = parser.parse_args()

metadata = {}
reading_header = False
reading_data = False
next_data_bucket = None

def debug(message):
  if args.verbose:
    print '[DEBUG] %s' % message
  return

with open(args.fifo) as f:
  for line in f:
    if reading_header:
      debug('This line is a data header')

      if not '<data encoding="base64">' in line:
        print 'Error: Expected base64 header, got %s' % line

      reading_header = False
      reading_data = True
      continue

    elif reading_data:
      debug('This line is data')

      if next_data_bucket:
        datum_match = re.match('([a-zA-Z0-9+]+={0,2})<\/data>', line, flags=re.IGNORECASE)
        if datum_match:
          datum = datum_match.groups()[0].decode('base64')
          metadata[next_data_bucket] = datum
          debug('Stored data "%s" in bucket "%s"' % (datum, next_data_bucket))
        else:
          print 'Error: Expected data, got %s' % line
      else:
        debug('Dropped data on the floor')

      reading_data = False
      continue

    else:
      tag_match = re.match('<type>(\w+)<\/type><code>(\w+)<\/code><length>(\d+)<\/length>', line, flags=re.IGNORECASE)
      if tag_match:
        debug('This line is a tag')
        type_hex, code_hex, length_string = tag_match.groups()
        type = type_hex.decode('hex')
        code = code_hex.decode('hex')
        length = int(length_string)

        # if code == 'mdst':
        #   # Metadata start
        #   # Sanity check - this shouldn't normally be necessary
        #   debug('Clearing metadata (start)')
        #   metadata = {}
        # elif code == 'mden':
        if code == 'mden':
          # Metadata end
          # Magic from http://stackoverflow.com/a/6117124/821471
          replace = dict((re.escape('%' + k), v) for k, v in metadata.iteritems())
          pattern = re.compile('|'.join(replace.keys()))
          formatted = pattern.sub(lambda m: replace[re.escape(m.group(0))], args.format)
          print formatted.decode('string_escape')

          metadata = {}
          debug('Cleared metadata')

        if length > 0:
          bucket = None

          if code == 'asal':
            bucket = 'album'
          elif code == 'asar':
            bucket = 'artist'
          elif code == 'ascm':
            bucket = 'comment'
          elif code == 'asgm':
            bucket = 'genre'
          elif code == 'minm':
            bucket = 'title'
          elif code == 'ascp':
            bucket = 'composer'

          next_data_bucket = bucket
          reading_header = True
          continue
        # elif length 0
      else:
        print 'Error: Expected tag, got %s' % line
