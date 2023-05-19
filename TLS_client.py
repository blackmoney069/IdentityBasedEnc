import socket
import ssl

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

secure_socket = ssl_context.wrap_socket(normal_socket, server_side=False, server_hostname="localhost")
secure_socket.connect(("localhost",3002))

print(secure_socket.recv(1024).decode())

normal_socket.close()
