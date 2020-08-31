import sys
import socket

table = {}
ts_hostname = ""

with open("PROJI-DNSRS.txt") as f:
    for line in f:
        if len(line.split()) < 3:
            break

        (addr, ip, type) = line.split()
        if type == "A":
            table[addr] = ip
        else:
            ts_hostname = addr
print "[RS]: Table construction complete, TSHostName: " + ts_hostname

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[RS]: Server socket created"
except socket.error as err:
    print '[RS]: socket open error: {}\n'.format(err)
    exit()

server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)
ss.listen(1)
csockid, add = ss.accept()
print "[RS]: Connection received from: {}".format(add)

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
        print "[RS]: Successful lookup for: " + request + ", sent: " + msg
    else:
        msg = ts_hostname + " - NS"
        print "[RS]: Failed lookup for: " + request + ", sent: " + msg

    csockid.send(msg.encode('utf-8'))

