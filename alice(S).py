import socket
import random
import ssl
import core.tools as tools
import core.encryptionScheme as encryption


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
secure_socket.send("CLOSE".encode())
print(authority_MPK, "AUTH MPK")
secure_socket.close()
# Alice connected with authority to get the MPK

recv_identity = input("Please enter the receiver identity")
hashed_recv_id = tools.hashIdentity(recv_identity, authority_MPK)

alice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_socket.connect(("localhost", 3003))

# alice is now connected to bob, handshakes can be done
connection_key_int = random.getrandbits(32)
# this is the connection key and this will be sent to bob using Identity Based Encryption
print(connection_key_int, "INT CONN KEY")

connection_key_bin = (bin(connection_key_int)[2:]).zfill(32)
print(connection_key_bin, "BINARY")

encrypted_key = encryption.encrypt(connection_key_bin, authority_MPK, hashed_recv_id)
# print(str(encrypted_key), "STR")
# print(encrypted_key, "LIS")
# while True:

print("Connected to reciever")
alice_socket.send(("|"+str(encrypted_key)+"|").encode())
print("Key sent!")


alice_socket.close()
