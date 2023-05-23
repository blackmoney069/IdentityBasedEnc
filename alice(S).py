import socket
import random


try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations("./certificates/authCert.crt")

secure_socket = ssl_context.wrap_socket(normal_socket, server_side=False, server_hostname="localhost")
# secure_socket = ssl.wrap_socket(normal_socket, server_side=False)
secure_socket.connect(("localhost",3002))

print(secure_socket.recv(1024).decode())
print(secure_socket.recv(1024).decode())
print(secure_socket.recv(1024).decode())
print(secure_socket.recv(1024).decode())
print(secure_socket.recv(1024).decode())

authority_MPK = int(secure_socket.recv(1024).decode())
print(authority_MPK, "AUTH MPK")
secure_socket.close()
# Alice connected with authority to get the MPK

recv_identity = input("Please enter the receiver identity")

alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket.connect(("localhost", 3003))

# alice is now connected to bob, handshakes can be done
connection_key = random.randint(10000000, 99999999)
# this is the connection key and this will be sent to bob using Identity Based Encryption


while True:


    print(alice_socket.recv(1024).decode())

alice_socket.close()
