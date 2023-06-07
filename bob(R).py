import socket
import ssl
import core.decryptionScheme as decryptionScheme
import core.tools as tools
from cryptography.fernet import Fernet
import base64

COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[32m'
COLOR_BLUE = '\033[34m'

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
    print("Bob listening to alice at", addr)

    #  now the key exchange will happen
    print("Alice is now sending encrypted connection key")
    encrypted_str = conn.recv(10240).decode()
    print("Encrypted Communication can start, enter 'baskar()' to exit chat")
    encrypted_list = eval(encrypted_str.split("|")[1])
    connection_key = decryptionScheme.decrypt_sequence(encrypted_list, int(secret_key), hashed_id, authority_MPK)
   
    # connection key is retrieved and now symmtric encryption can be used
    fernetKey = base64.urlsafe_b64encode(tools.bits_to_key(connection_key))
    fernetObject = Fernet(fernetKey)

    # fernet object created for encryption and decryption
    print("------------------")
    while(True):
        rec = conn.recv(1024).decode()
        if(fernetObject.decrypt(rec).decode().lower()=="baskar()"):
            break
        print(COLOR_GREEN + "ALICE : {}".format(fernetObject.decrypt(rec).decode())+ COLOR_RESET)
        BobIn = input(COLOR_BLUE + "BOB : ")
        print(COLOR_RESET, end="")
        if(BobIn.lower()=="baskar()"):
            encryptedMessage = fernetObject.encrypt(BobIn.encode())
            conn.send(encryptedMessage)
            break
        encryptedMessage = fernetObject.encrypt(BobIn.encode())
        conn.send(encryptedMessage)

