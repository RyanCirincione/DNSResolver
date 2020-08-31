import sys
import socket

table = {}

with open("PROJ2-DNSTScom.txt") as f:
    for line in f:
        if len(line.split()) < 3:
            break

        (addr, ip, type) = line.split()
        table[addr] = ip
print "[TSC]: Table construction complete"

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TSC]: Server socket created")
except socket.error as err:
    print('[TSC]: socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)
ss.listen(1)
csockid, add = ss.accept()
print "[TSC]: Connection received from: {}".format(add)

while True:
    request = csockid.recv(200).decode('utf-8')
    entry = ""

    for addr in table:
        if addr.lower() == request.lower():
            entry = addr
            break

    msg = ""
    if entry != "":
        msg = request + " " + table[entry] + " A"
        print "[TSC]: Successful lookup for: " + request + ", sent: " + msg
    else:
        msg = request + " - Error:HOST NOT FOUND"
        print "[TSC]: Failed lookup for: " + request + ", sent: " + msg

    csockid.send(msg.encode('utf-8'))

