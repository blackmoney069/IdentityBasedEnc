import socket

try:
    normal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

normal_socket.bind(("",3002))
print("Normal Socket is binded to 3001")

normal_socket.listen(5)
# now the socket will listen to calls from the network

while True:
    conn, addr = normal_socket.accept()
    print("Got a connection from", addr)

    conn.send("Thanks for connecting".encode())
    conn.close()

    break