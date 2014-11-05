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

reciever, addr = sock.accept()


while True:
  shape = reciever.recv(13)
  count = int(reciever.recv(2))
  print shape, count
  splitted = shape.split(',')
  x1 = int(splitted[0][1:])
  x2 = int(splitted[1][1:])
  x3 = int(splitted[2][:len(splitted[2])-1])
  
  
  buf = ''
  for i in range(count):
    buf = buf + reciever.recv(20480)
  buf = buf + reciever.recv(x1*x2*x3 - 20480*count)
  #buf = buf[:x1*x2*x3]
  print len(buf)
  aar = []
  for ch in buf:
    aar.append(ord(ch))

  arr = np.array(aar)
  print arr.size
  ppp = arr.reshape((x1, x2, x3))

  cv.imshow('recieved_image', ppp)
  if cv.waitKey(1) & 0xFF == ord('q'):
    break
  print 'accepted'

reciever.close()

print time.time()-start
