import socket
import ssl

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='authCert.crt', keyfile="server.key")

normal_socket.bind(("",3002))
print("Normal Socket is binded to 3001")

normal_socket.listen(5)
ssl_socket = ssl_context.wrap_socket(normal_socket, server_side=True)
# now the socket will listen to calls from the network
print("Secure Socket is binded to 3002")

while True:
    conn, addr = ssl_socket.accept()
    print("Got a connection from", addr)

    conn.send("Thanks for connecting".encode())
    conn.close()

    break