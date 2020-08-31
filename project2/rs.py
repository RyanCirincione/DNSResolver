import sys
import socket

table = {}
com_hostname = ""
edu_hostname = ""

with open("PROJ2-DNSRS.txt") as f:
    for line in f:
        if len(line.split()) < 3:
            break

        (addr, ip, type) = line.split()
        if type == "A":
            table[addr] = ip
        else:
            if addr.endswith(".com"):
                com_hostname = ip
            else:
                edu_hostname = ip
print "[RS]: Table construction complete, com hostname: " + com_hostname + ", edu hostname: " + edu_hostname

# _____ TS COM CONNECTION _____
try:
    com_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print('[RS] socket open error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the server
com_port = int(sys.argv[3])
com_addr = socket.gethostbyname(com_hostname)

# connect to the server on local machine
server_binding = (com_addr, com_port)
com_socket.connect(server_binding)

# _____ TS EDU CONNECTION _____
try:
    edu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print('[RS] socket open error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the server
edu_port = int(sys.argv[2])
edu_addr = socket.gethostbyname(edu_hostname)

# connect to the server on local machine
server_binding = (edu_addr, edu_port)
edu_socket.connect(server_binding)

# _____ CLIENT CONNECTION _____
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "[RS]: Server socket created"
except socket.error as err:
    print '[RS]: socket open error: {}\n'.format(err)
    exit()

server_binding = ('', int(sys.argv[1]))
client_socket.bind(server_binding)
client_socket.listen(1)
csockid, add = client_socket.accept()
print "[RS]: Connection received from: {}".format(add)

while True:
    request = csockid.recv(200).decode('utf-8')
    entry = ""

    for addr in table:
        if addr.lower() == request.lower():
            entry = addr
            break

    msg = ""
    if entry != "":
        msg = entry + " " + table[entry] + " A"
        print "[RS]: Successful lookup for: " + request + ", sent: " + msg
    else:
        if request.lower().endswith(".com"):
            com_socket.send(request.encode('utf-8'))
            msg = com_socket.recv(200).decode('utf-8')
            print "[RS]: Successfully asked TS COM for: " + request + ", echoing message: " + msg
        elif request.lower().endswith(".edu"):
            edu_socket.send(request.encode('utf-8'))
            msg = edu_socket.recv(200).decode('utf-8')
            print "[RS]: Successfully asked TS EDU for: " + request + ", echoing message: " + msg
        else:
            msg = request + " - Error:HOST NOT FOUND"
            print "[RS]: Failed lookup for: " + request + ", sent: " + msg

    csockid.send(msg.encode('utf-8'))

