import socket
import core.decryptionScheme as decryptionScheme
import core.tools as tools
from cryptography.fernet import Fernet
import base64

COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[32m'
COLOR_BLUE = '\033[34m'


AUTH_IP_ADDR = "127.0.0.1"
AUTH_PORT = 3002

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))


# secure_socket = ssl.wrap_socket(normal_socket, server_side=False)
normal_socket.connect((AUTH_IP_ADDR, AUTH_PORT))

print(normal_socket.recv(2048).decode())

authority_MPK = int(normal_socket.recv(1024).decode())
print(COLOR_GREEN + "Recieved AUTH MPK", authority_MPK, COLOR_RESET)

identity =  input("Identity: ")
hashed_id = tools.hashIdentity(identity, authority_MPK)

normal_socket.send(identity.encode())

print(normal_socket.recv(1024).decode())
secret_key = normal_socket.recv(1024).decode()

normal_socket.close()

#  Now bob has received its secret key and alice can send any data to it now:

try:
    bob_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

BOB_IP_ADDR = "127.0.0.1"
BOB_PORT = 3003

bob_socket.bind(('0.0.0.0', 3003))
bob_socket.listen(1)
print("Bob is now open to encrypted Communication")


while True:
    listen = input("Do you want to continue listening?(Y/N)")
    if(listen=="N"):
        bob_socket.close()
        break

    print("To connect, use the following IP and port : ", BOB_IP_ADDR, BOB_PORT)
    conn, addr = bob_socket.accept()
    print("You are connected to", addr)

    #  now the key exchange will happen
    print("Sender is now sending encrypted connection key")
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
        print(COLOR_GREEN + "SENDER : {}".format(fernetObject.decrypt(rec).decode())+ COLOR_RESET)
        BobIn = input(COLOR_BLUE + "ME : ")
        print(COLOR_RESET, end="")
        if(BobIn.lower()=="baskar()"):
            encryptedMessage = fernetObject.encrypt(BobIn.encode())
            conn.send(encryptedMessage)
            break
        encryptedMessage = fernetObject.encrypt(BobIn.encode())
        conn.send(encryptedMessage)

