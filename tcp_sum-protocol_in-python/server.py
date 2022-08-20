"""
Autor: Konrad Pasternak
Data: 22.04.2022
"""

import selectors, socket, sys
HOST = "127.0.0.1"
DEFAULT_PORT = 2020
BUFFER_SIZE = 1024
MAX = 4294967295

slctor = selectors.DefaultSelector()
clients = {}

class Client:
  def __init__(self):
    self.stack = []
    self.flag_overflow = False
    self.flag_wrong_char = False
    self.previous_character = 0
  def stack_pop(self):
    return self.stack.pop()
  def stack_push(self, e):
    self.stack.append(e)
  def clear_stack(self):
    self.stack.clear()
  def get_stack(self):
    return self.stack
  def get_stack_len(self):
    return len(self.stack)
  def get_flag_overflow(self):
    return self.flag_overflow
  def get_flag_wrong_char(self):
    return self.flag_wrong_char
  def get_previous_character(self):
    return self.previous_character
  def set_flag_overflow(self, e):
    self.flag_overflow = e
  def set_flag_wrong_char(self, e):
    self.flag_wrong_char = e
  def set_previous_character(self, e):
    self.previous_character = e

class Encryptor:
  def __init__(self, slctor, sock):
    slctor.register(sock, selectors.EVENT_READ, data=self)
    clients[sock] = Client()
    self.selector = slctor
    self.socket = sock
  def read(self):
    data = self.socket.recv(BUFFER_SIZE)
    if len(data) == 0:
      self.close()
    else:
      data = encode(data, self.socket)
      self.socket.send(bytes(data))
  def close(self):
    self.selector.unregister(self.socket)
    self.socket.close()

class Listener:
  def __init__(self, slctor, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, port))
    sock.listen(10)
    slctor.register(sock, selectors.EVENT_READ, data=self)
    self.selector = slctor
    self.socket = sock
  def read(self):
    conn, addr = self.socket.accept()
    Encryptor(self.selector, conn)
  def close(self):
    self.selector.unregister(self.socket)
    self.socket.close()

def encode(buffer, sock):
  client = clients[sock]
  msg = ""
  for character in buffer:
    prev = client.get_previous_character()
    if prev == 13 and character == 10:
      if client.get_stack_len() == 0: msg += "ERROR\r\n"
      else:
        if client.get_flag_wrong_char():
          msg += "ERROR\r\n"
          client.set_flag_overflow(False)
          client.set_flag_wrong_char(False)
          client.clear_stack()
        else:
          summation = 0
          for e in ''.join(client.get_stack()).split(' '):
            if e == '':
              client.set_flag_overflow(True)  # Stworzyc nowa flage z inna nazwa
            else:
              e = int(e)
              if e >= MAX: client.set_flag_overflow(True)
              elif summation >= MAX - e: client.set_flag_overflow(True)
              summation += e
          client.clear_stack()
          if client.get_flag_overflow():
            msg += "ERROR\r\n"
            client.set_flag_overflow(False)
            client.set_flag_wrong_char(False)
          else: msg += str(summation) + "\r\n"
    elif (48 <= character and character <= 57) or character == 32:
      client.stack_push(chr(character))
    elif character != 13:
      client.set_flag_wrong_char(True)
    client.set_previous_character(character)
  return bytes(msg, 'ascii')

if len(sys.argv) <= 1:
  Listener(slctor, DEFAULT_PORT)
else:
  for arg in sys.argv[1:]:
    Listener(slctor, int(arg))

while True:
  ready_list = slctor.select(timeout=180)
  if len(ready_list) == 0:
    break
  for key, event in ready_list:
    if event | selectors.EVENT_READ > 0:
      key.data.read()