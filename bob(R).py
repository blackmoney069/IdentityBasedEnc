import socket
import ssl
import core.decryption as decryption
import core.tools as tools

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

identity =  input("Identity: ")
hashed_id = tools.hashIdentity(identity, authority_MPK)

secure_socket.send(identity.encode())

print(secure_socket.recv(1024).decode())
secret_key = secure_socket.recv(1024).decode()
print(secret_key, "SEC KEY")

secure_socket.close()

#  Now bob has received its secret key and alice can send any data to it now:

try:
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

bob_socket.bind(('localhost', 3003))
bob_socket.listen(1)
print("Bob is now open to encrypted Communication")


while True:
    listen = input("Do you want to continue listening?(Y/N)")
    if(listen=="N"):
        bob_socket.close()
        break

    conn, addr = bob_socket.accept()
    print("Bob listening to", addr)

    #  now the key exchange will happen
    conn.send("Hi from Bob".encode())
    print(conn.recv(1024).decode())
    encrypted_str = conn.recv(1024).decode()
    print(conn.recv(1024).decode())
    encrypted_list = eval(encrypted_str)
    connection_key = decryption.decrypt_sequence(encrypted_list, secret_key, hashed_id, authority_MPK)
    print(connection_key, "CONN KEY")

    
