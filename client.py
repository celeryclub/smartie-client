import argparse, sys, socket, json
from ssnc import watch

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--host', required=True)
parser.add_argument('-p', '--port', type=int)
# parser.add_argument('-v', '--verbose', action='count')
parser.add_argument('fifo')
args = parser.parse_args()

HOST = args.host
PORT = args.port or 8089

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client.connect((HOST, PORT))
reply = client.recv(1024).decode()
print(reply)

line_buf = {}

def send_message(message):
  data = json.dumps(message)
  print(repr('sending data'))
  print(repr(data))
  client.send(data.encode())
  reply = client.recv(1024).decode()
  print(reply)

def set_line(data, line):
  global line_buf
  line_buf['line' + str(line)] = data

def flush_lines(skip_backlight=False):
  global line_buf
  print(repr('flushing'))
  send_message(line_buf)
  if not skip_backlight:
    backlight_on()
  line_buf = {}

def clear_screen():
  set_line('', 1)
  set_line('', 2)
  set_line('', 3)
  set_line('', 4)
  flush_lines(True)

def backlight_on():
  print('backlight_on')
  send_message({ 'backlight': 'on' })

def backlight_off():
  print('backlight_off')
  send_message({ 'backlight': 'off' })
  clear_screen()

def debug_log(message, level=1):
  # if args and args.verbose and args.verbose >= level:
    # print('[DEBUG] %s' % message)
  # return
  print('[DEBUG] %s' % message)

try:
  watch(args.fifo, set_line, flush_lines, backlight_off, debug_log)
except KeyboardInterrupt:
  sys.stdout.flush()
