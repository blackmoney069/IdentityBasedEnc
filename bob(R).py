import socket
import ssl
import core.decryptionScheme as decryptionScheme
import core.tools as tools
from cryptography.fernet import Fernet
import base64
import netifaces
import yaml

COLOR_RESET = '\033[0m'
COLOR_GREEN = '\033[32m'
COLOR_BLUE = '\033[34m'

with open('config.yaml','r') as config:
    data = yaml.safe_load(config)

AUTH_IP_ADDR = data['pkg']['ip']
AUTH_PORT = data['pkg']['port']

interfaces = netifaces.interfaces()

for interface in interfaces:
    addresses = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addresses:
        ip_addresses = [addr['addr'] for addr in addresses[netifaces.AF_INET]]
        if(ip_addresses[0][:9]=="10.10.100"):
            BOB_IP_ADDR = ip_addresses[0]

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations("./certificates/ca_certificate.pem")

secure_socket = ssl_context.wrap_socket(normal_socket, server_side=False, server_hostname=data['pkg']['hostname'])
# secure_socket = ssl.wrap_socket(normal_socket, server_side=False)
secure_socket.connect((AUTH_IP_ADDR, AUTH_PORT))

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

bob_socket.bind(('0.0.0.0', 3002))
bob_socket.listen(1)
print("Bob is now open to encrypted Communication")


while True:
    listen = input("Do you want to continue listening?(Y/N)")
    if(listen=="N"):
        bob_socket.close()
        break

    print("To connect, use the following IP : ", BOB_IP_ADDR)
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

