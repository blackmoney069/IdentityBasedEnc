import socket

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

normal_socket.connect(("localhost",3002))

print(normal_socket.recv(1024).decode())

normal_socket.close()
