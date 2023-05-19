import socket

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))


socket.bind(("",3001))
socket.listen(1)

while True:
    conn, addr = socket.accept()
    conn.send("This is nice".encode())

    conn.close()

    break