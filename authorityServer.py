import socket
import ssl
import core.authorityRoles as authorityRoles

# Define IP Addresses and PORTS
AUTH_IP_ADDR = '0.0.0.0'
AUTH_PORT = 3002

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='./certificates/ca_certificate.pem', keyfile="./certificates/ca_private_key.pem")


# create an instance of authority
auth = authorityRoles.Authority()


normal_socket.bind((AUTH_IP_ADDR,AUTH_PORT))
normal_socket.listen(5)
ssl_socket = ssl_context.wrap_socket(normal_socket, server_side=True)
# now the socket will listen to calls from the network
print("Authority is listening securely at IP {} PORT {}".format(AUTH_IP_ADDR, AUTH_PORT))

while True:
    conn, addr = ssl_socket.accept()
    print("Got a connection from", addr)

    # Authority sends public data and welcome message to user
    conn.send(bytes("---------------------------------",'utf-8'))
    conn.send(bytes("Welcome to Central Authority",'utf-8'))
    conn.send(bytes("---------------------------------\n",'utf-8'))
    conn.send(bytes("|| Public Parameters || M = {} || ".format(auth.send_MPK()),'utf-8'))
    conn.send(bytes("Please enter your identity",'utf-8'))
    conn.send(bytes("{}".format(auth.send_MPK()),'utf-8'))
    identity = conn.recv(1024).decode('utf-8')
    if(identity=="CLOSE"):
        conn.close()
    else:
    # identity recieved as string from the client
        conn.send(bytes("---- Secret key for your use is sent || KEEP IT SAFE ----",'utf-8'))
        secret_key  = auth.keyGeneration(identity_string=identity)
        print(secret_key)
        conn.send(bytes(str(secret_key),'utf-8'))

        conn.close()

ssl_socket.close()