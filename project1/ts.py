import sys
import socket

table = {}

with open("PROJI-DNSTS.txt") as f:
    for line in f:
        if len(line.split()) < 3:
            break

        (addr, ip, type) = line.split()
        table[addr] = ip
print "[TS]: Table construction complete"

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS]: Server socket created")
except socket.error as err:
    print('[TS]: socket open error: {}\n'.format(err))
    exit()

server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)
ss.listen(1)
csockid, add = ss.accept()
print "[TS]: Connection received from: {}".format(add)

while True:
    request = csockid.recv(200).decode('utf-8')
    entry = ""
    if request == "":
        break

    for addr in table:
        if addr.lower() == request.lower():
            entry = addr
            break

    msg = ""
    if entry != "":
        msg = entry + " " + table[entry] + " A"
        print "[TS]: Successful lookup for: " + request + ", sent: " + msg
    else:
        msg = request + " - Error:HOST NOT FOUND"
        print "[TS]: Failed lookup for: " + request + ", sent: " + msg

    csockid.send(msg.encode('utf-8'))

csockid.close()
