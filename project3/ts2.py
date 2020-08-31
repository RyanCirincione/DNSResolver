import sys
import socket
import hmac

table = {}

with open("PROJ3-DNSTS2.txt") as f:
    for line in f:
        if len(line.split()) < 3:
            break

        (addr, ip, type) = line.split()
        table[addr] = ip
print "[TS2]: Table construction complete"

key = ""

with open("PROJ3-KEY2.txt") as f:
    for line in f:
        key = line.replace("\n", "")
        break
print "[TS2]: Key: " + key

# OPEN SOCKET FOR AS
try:
    sA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS2]: Server socket created")
except socket.error as err:
    print('[TS2]: socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(sys.argv[1]))
sA.bind(server_binding)
sA.listen(1)
socketA, add = sA.accept()
print "[TS2]: AS connection received from: {}".format(add)

clientConnected = False
while True:
    # Receive challenge from AS
    challenge = socketA.recv(200).decode('utf-8')
    print "[TS2]: Received challenge from AS: " + challenge

    # Reply with digest to AS
    digest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8")).hexdigest()
    socketA.send(digest.encode('utf-8'))
    print "[TS2]: Sending digest: " + digest

    # AS informs whether we are the target TS, and if so prepare for client request
    success = socketA.recv(200).decode('utf-8')
    if success == "S":
        if not clientConnected:
            # OPEN SOCKET FOR CLIENT
            try:
                ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[TS2]: Server socket created")
            except socket.error as err:
                print('[TS2]: socket open error: {}\n'.format(err))
                exit()

            server_binding = ('', int(sys.argv[2]))
            ss.bind(server_binding)
            ss.listen(1)
            socketC, add = ss.accept()
            print "[TS2]: Client connection received from: {}".format(add)
	    clientConnected = True

        request = socketC.recv(200).decode('utf-8')
        entry = ""

        for addr in table:
            if addr.lower() == request.lower():
                entry = addr
                break

        msg = ""
        if entry != "":
            msg = entry + " " + table[entry] + " A"
            print "[TS1]: Successful lookup for: " + request + ", sent: " + msg
        else:
            msg = request + " - Error:HOST NOT FOUND"
            print "[TS1]: Failed lookup for: " + request + ", sent: " + msg

        socketC.send(msg.encode('utf-8'))

