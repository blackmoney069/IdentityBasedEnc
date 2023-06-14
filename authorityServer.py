import socket
import ssl
import core.authorityRoles as authorityRoles
import yaml

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='./certificates/ca_certificate.pem', keyfile="./certificates/ca_private_key.pem")


# create an instance of authority
auth = authorityRoles.Authority()


normal_socket.bind(("0.0.0.0",3002))
normal_socket.listen(5)
ssl_socket = ssl_context.wrap_socket(normal_socket, server_side=True)

with open('config.yaml', "r") as config:
    data = yaml.safe_load(config)

# Define IP Addresses and PORTS
AUTH_IP_ADDR = socket.gethostbyname(socket.gethostname())
AUTH_PORT = 3002

data['pkg']['ip'] = AUTH_IP_ADDR
data['pkg']['hostname'] = socket.gethostname()

with open('config.yaml', "w") as config:
    yaml.safe_dump(data, config)


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