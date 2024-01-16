import socket
import core.authorityRoles as authorityRoles

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

# create an instance of authority
auth = authorityRoles.Authority()

normal_socket.bind(("0.0.0.0",3002))
normal_socket.listen(5)



# Define IP Addresses and PORTS
# AUTH_IP_ADDR = socket.gethostbyname(socket.gethostname())
AUTH_IP_ADDR = "0.0.0.0"
AUTH_PORT = 3002

# now the socket will listen to calls from the network
print("Authority is listening securely at IP {} PORT {}".format(AUTH_IP_ADDR, AUTH_PORT))

while True:
    conn, addr = normal_socket.accept()
    print("Got a connection from", addr)

    # Authority sends public data and welcome message to user
    conn.send(bytes("---------------------------------Welcome to Central Authority---------------------------------\n|| Public Parameters || M = {} || Please enter your identity".format(auth.send_MPK()),'utf-8'))
    print("Sending auth Master Public Key")
    conn.send(bytes("{}".format(auth.send_MPK()),'utf-8'))
    identity = conn.recv(1024).decode('utf-8')
    if(identity=="CLOSE"):
        conn.close()
    else:
    # identity recieved as string from the client
        conn.send(bytes("---- Secret key for your use is sent || KEEP IT SAFE ----",'utf-8'))
        secret_key  = auth.keyGeneration(identity_string=identity)
        # print(secret_key)
        conn.send(bytes(str(secret_key),'utf-8'))

        conn.close()

ssl_socket.close()