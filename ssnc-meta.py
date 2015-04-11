#!/usr/bin/python -u

# Usage:
# python -u ssnc-meta.py -f '%title\n%artist\n%album\n' -c '%I:%M:%S %p\n\n\n' test/meta.xml

import sys, argparse, re, time
from clock import Clock

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', required=True)
parser.add_argument('-e', '--endscreen')
parser.add_argument('-c', '--clock')
parser.add_argument('-v', '--verbose', action='count')
parser.add_argument('fifo')
args = parser.parse_args()

metadata = {}
reading_header = False
reading_data = False
next_data_bucket = None
ticker = None

def debug(message, level=1):
  if args.verbose and args.verbose >= level:
    print '[DEBUG] %s' % message
  return

def start_clock():
  global ticker
  ticker = Clock(args.clock)
  ticker.start()
  debug('Started the clock')

def stop_clock():
  global ticker
  if ticker and ticker.isAlive():
    ticker.stop()
    ticker.join()
    debug('Stopped the clock')

try:
  if args.clock: start_clock()

  fifo = open(args.fifo, 'r')
  with fifo as f:
    while True:
      line = f.readline()
      if line == '':
        debug('Reached EOF', 2)
        break

      if reading_header:
        debug('This line is a data header', 2)

        if not '<data encoding="base64">' in line:
          print 'Error: Expected base64 header, got "%s"' % line

        reading_header = False
        reading_data = True
        continue

      elif reading_data:
        debug('This line is data', 2)

        if next_data_bucket:
          datum_match = re.match('([a-zA-Z0-9+\/]+={0,2})<\/data>', line, flags=re.IGNORECASE)
          if datum_match:
            datum = datum_match.groups()[0].decode('base64')
            metadata[next_data_bucket] = datum
            debug('Stored "%s" as "%s"' % (datum, next_data_bucket))
          else:
            print 'Error: Expected data, got "%s"' % line
        else:
          debug('Dropped data on the floor', 2)

        reading_data = False
        continue

      else:
        tag_match = re.match('<type>(\w+)<\/type><code>(\w+)<\/code><length>(\d+)<\/length>', line, flags=re.IGNORECASE)
        if tag_match:
          debug('This line is a tag', 2)
          type_hex, code_hex, length_string = tag_match.groups()
          type = type_hex.decode('hex')
          code = code_hex.decode('hex')
          length = int(length_string)

          if code == 'pend':
            # Play stream end
            if args.clock:
              start_clock()
              continue
            elif args.endscreen:
              print args.endscreen.decode('string_escape')
              debug('Printed endscreen')
              continue

          elif code == 'mden':
            # Metadata block end
            if args.clock: stop_clock()
            # Magic from http://stackoverflow.com/a/6117124/821471
            replace = dict((re.escape('%' + k), v) for k, v in metadata.iteritems())
            pattern = re.compile('|'.join(replace.keys()))
            formatted = pattern.sub(lambda m: replace[re.escape(m.group(0))], args.format)
            print formatted.decode('string_escape')

            metadata = {}
            debug('Cleared metadata')

          elif length > 0:
            bucket = None

            if code == 'asal':
              bucket = 'album'
            elif code == 'asar':
              bucket = 'artist'
            elif code == 'ascm':
              bucket = 'comment'
            elif code == 'asgm':
              bucket = 'genre'
            elif code == 'ascp':
              bucket = 'composer'
            elif code == 'minm':
              bucket = 'title'

            next_data_bucket = bucket
            reading_header = True
            continue
        else:
          print 'Error: Expected tag, got "%s"' % line
except KeyboardInterrupt:
  stop_clock()
  sys.stdout.flush()
