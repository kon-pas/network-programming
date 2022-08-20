import socket
HOST = "127.0.0.1"
BUFFER_SIZE = 1024
PORT_0 = 2020

TCP_CLIENT_SOCKET_0 = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCP_CLIENT_SOCKET_0.connect((HOST, PORT_0))
TCP_CLIENT_SOCKET_0.send(b"\r\n")
print(TCP_CLIENT_SOCKET_0.recv(BUFFER_SIZE))
