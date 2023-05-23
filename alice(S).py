import socket

recv_identity = input("Please enter the receiver identity")

alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

alice_socket.connect(("localhost", 3003))

print(alice_socket.recv(1024).decode())

alice_socket.close()
