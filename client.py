import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

sock.connect(("localhost",3001))

print(sock.recv(1024).decode())

sock.close()