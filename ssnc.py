import sys, argparse, re

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--format', required=True)
  parser.add_argument('-e', '--endscreen')
  parser.add_argument('-v', '--verbose', action='count')
  parser.add_argument('fifo')
  args = parser.parse_args()

def debug(message, level=1):
  if args.verbose and args.verbose >= level:
    print('[DEBUG] %s' % message)
  return

def main():
  metadata = {}
  reading_header = False
  reading_data = False
  next_data_bucket = None


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
          print('Error: Expected base64 header, got "%s"' % line)

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
            print('Error: Expected data, got "%s"' % line)
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
            if args.endscreen:
              print(args.endscreen.decode('string_escape'))
              debug('Printed endscreen')
              continue

          elif code == 'mden':
            # Metadata block end
            # Magic from http://stackoverflow.com/a/6117124/821471
            replace = dict((re.escape('%' + k), v) for k, v in metadata.iteritems())
            pattern = re.compile('|'.join(replace.keys()))
            try:
              formatted = pattern.sub(lambda m: replace[re.escape(m.group(0))], args.format)
            except KeyError:
              print('ERROR')
              print(replace)
              print(replace.keys())
              print('end')
            print(formatted.decode('string_escape'))

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
          print('Error: Expected tag, got "%s"' % line)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    sys.stdout.flush()
