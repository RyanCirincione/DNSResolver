import threading
import time
import random
import sys


import socket


try:
	cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # getservbyName()
    	print "[C]: Client socket 2 created"
except socket.error as err:
    	print 'socket open error: {} \n'.format(err)
    	exit()

#ts.gethostbyname(localhost) #change later
port2 = int(sys.argv[3]) #50622
#localhost_addr = socket.gethostbyname(sys.argv[1))

try:
    	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # getservbyName()
    	print "[C]: Client socket created"
except socket.error as err:
    	print 'socket open error: {} \n'.format(err)
    	exit()
	localhost_addr = socket.gethostbyname(sys.argv[1])
	
#ts.gethostbyname(localhost) #change later
port = int(sys.argv[2]) #50621
localhost_addr = socket.gethostbyname(sys.argv[1]) 

# connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)


array = []

with open("PROJI-HNS.txt") as f: #Change for testing 
    for line in f:
        array.append(line.replace("\n", ""))
		
print(array)
b = False

with open("RESOLVED.txt", "w+") as g:
	for x in array:
		if x == "":
			continue

		cs.send(x.encode('utf-8'))
		data_from_server=cs.recv(200).decode('utf-8')
		print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

		if data_from_server.split()[2] == "NS":
			if not b:
				localhost_addr = socket.gethostbyname(data_from_server.split()[0])
				server_binding = (localhost_addr, port2)
				cs2.connect(server_binding)
				b = True
			cs2.send(x.encode('utf-8'))
			data_from_server= cs2.recv(200).decode('utf-8')
		g.write(data_from_server + "\n") 
	else:
		print("done")

#Search for rsHostName
#if(rsHostName == True)
    # return

cs2.close()
cs.close()
exit()

