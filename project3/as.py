import sys
import socket

# _____ TS1 CONNECTION _____
try:
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print('[AS] socket open error: {} \n'.format(err))
    exit()

ts1_hostname = sys.argv[2]
addr1 = socket.gethostbyname(ts1_hostname)

server_binding = (addr1, int(sys.argv[3]))
socket1.connect(server_binding)

# _____ TS2 CONNECTION _____
try:
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print('[AS] socket open error: {} \n'.format(err))
    exit()

ts2_hostname = sys.argv[4]
addr2 = socket.gethostbyname(ts2_hostname)

server_binding = (addr2, int(sys.argv[5]))
socket2.connect(server_binding)

# _____ CLIENT CONNECTION _____
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[AS]: Server socket created"
except socket.error as err:
    print '[AS]: socket open error: {}\n'.format(err)
    exit()

server_binding = ('', int(sys.argv[1]))
socket.bind(server_binding)
socket.listen(1)
socketC, add = socket.accept()
print "[AS]: Connection received from: {}".format(add)

while True:
    # Receive challenge and digest from client
    request = socketC.recv(200).decode('utf-8')
    challenge, digest = request.split(" ")
    print "[AS]: Received challenge + digest: " + challenge + ", " + digest

    # Send challenge to ts
    socket1.send(challenge.encode('utf-8'))
    print "[AS]: Sent 1/2"
    socket2.send(challenge.encode('utf-8'))
    print "[AS]: Sent 2/2"

    # Receive digests and determine which ts is correct
    digest1 = socket1.recv(200).decode('utf-8')
    digest2 = socket2.recv(200).decode('utf-8')
    print "[AS]: Received digests from TS1 + TS2: " + digest1 + ", " + digest2

    if digest1 == digest:
        # Inform ts of their success states
        socket1.send("S".encode('utf-8'))
        socket2.send("F".encode('utf-8'))

        # Inform client which ts to connect to and its hostname
        socketC.send(ts1_hostname + " 1")
        print "[AS]: Sending TS1 connection"
    else:
        # Inform ts of their success states
        socket1.send("F".encode('utf-8'))
        socket2.send("S".encode('utf-8'))

        # Inform client which ts to connect to and its hostname
        socketC.send(ts2_hostname + " 2")
        print "[AS]: Sending TS2 connection"

