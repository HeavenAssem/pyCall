import socket
import numpy as np
import binascii
import time
import sys
import cv2 as cv


start = time.time()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('', 9091))
sock.listen(1)

print time.time()-start
reciever, addr = sock.accept()

shape = reciever.recv(13)
count = reciever.recv(2)


splitted = shape.split(',')
x1, x2, x3 = int(splitted[0][1:]) , int(splitted[1][1:]) , int(splitted[2][:len(splitted[2])-1])

print time.time()-start

buf = ''
for i in range(int(count)+1):
  buf = buf + reciever.recv(20480)

aar = []
for ch in buf:
  aar.append(ord(ch))

arr = np.array(aar)
ppp = arr.reshape((x1, x2, x3))

cv.imwrite('recieved_image.jpg', ppp)

print ppp.shape

reciever.close()

print time.time()-start
