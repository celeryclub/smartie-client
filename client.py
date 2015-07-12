import argparse, sys, socket, json
from ssnc import watch

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--host')
parser.add_argument('-p', '--port', type=int)
# parser.add_argument('-v', '--verbose', action='count')
parser.add_argument('fifo')
args = parser.parse_args()

HOST = args.host or '10.0.1.4'
PORT = args.port or 8089

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client.connect((HOST, PORT))
reply = client.recv(1024).decode()
print(reply)

buf = {}

def set_line(data, line):
  global buf
  buf['line' + str(line)] = data

def flush():
  global buf
  print(repr('flushing'))
  data = json.dumps(buf)
  buf = {}
  print(repr(data))
  client.send(data.encode())
  reply = client.recv(1024).decode()
  print(reply)

def clear_screen():
  global buf
  buf['line1'] = 'clear'
  buf['line2'] = 'clear'
  buf['line3'] = 'clear'
  buf['line4'] = 'clear'
  flush()

def debug_log(message, level=1):
  # if args and args.verbose and args.verbose >= level:
    # print('[DEBUG] %s' % message)
  # return
  print('[DEBUG] %s' % message)

try:
  watch(args.fifo, set_line, flush, clear_screen, debug_log)
except KeyboardInterrupt:
  sys.stdout.flush()
