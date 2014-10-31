import socket
import numpy as np
import binascii
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('', 9091))
sock.listen(1)

reciever, addr = sock.accept()

shape = reciever.recv(13)

splitted = shape.split(',')
x1, x2, x3 = int(splitted[0][1:]) , int(splitted[1][1:]) , int(splitted[2][:len(splitted[2])-1])


#buf = buffer(reciever.recv(x1*x2*x3))
buf = buffer(reciever.recv(20480))

print x1, x2, x3, x1*x2*x3, sys.getsizeof(buf), len(buf)

aar = []
for ch in buf:
  aar.append(ord(ch))

arr = np.array(aar)
print type(aar), len(aar)
print type(arr), arr.size
#ppp = arr.reshape((x1, x2, x3))

#print len(ppp)

reciever.close()

