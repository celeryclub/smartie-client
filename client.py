import argparse, sys, socket

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--host')
parser.add_argument('-p', '--port', type=int)
args = parser.parse_args()

HOST = args.host or '10.0.1.5'
PORT = args.port or 8089

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client.connect((HOST, PORT))

reply = client.recv(1024).decode()
print(reply)

def send(message):
  print('sending ' + message + ' to server...')
  client.send(message.encode())
  reply = client.recv(1024).decode()
  print(reply)

  # while True:
    # client.recv(1024)
