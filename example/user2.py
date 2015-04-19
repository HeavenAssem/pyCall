import sys
import errno
import threading
import cv
import time
import socket
import numpy as np
import struct

block_size = 20240 #bytes



def transmitter(capture, connect_to):
  transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    transmit_socket.connect(connect_to)
  except socket.error, v:
    errorcode = v[0]
    if errorcode == errno.ECONNREFUSED:
      print "User you are trying to connect to is not online"
      exit()
    print threading.current_thread().name, "some error in socket", errorcode
    exit()
  
  while True:
    image = cv.QueryFrame(capture)
    if image != None:
      image = np.asarray(image[:,:])
      count = int(image.size/block_size)
      transmit_socket.send(struct.pack('iii', image.shape[0], image.shape[1], image.shape[2]))
      transmit_socket.send(struct.pack('i', count))
      for i in range(count):
        transmit_socket.send(image.data[block_size*i:block_size*(i+1)])
      transmit_socket.send(image.data[block_size*count:])
      if cv.WaitKey(1) & 0xFF == ord('q'):
        break
    
  transmit_socket.close()



def reciever():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('', 30091))
  sock.listen(1)
  
  print 'listening'
  recieve_socket, addr = sock.accept()
  print addr
  
  while True:
    shape = recieve_socket.recv(12)
    count = struct.unpack('i', recieve_socket.recv(4))[0]
    x1, x2, x3 = struct.unpack('iii', shape)
    
#    print x1, x2, x3, count#, len(buf)
    buf = ''
    for i in range(count):
      buf = ''.join([buf, recieve_socket.recv(block_size)])
    
    buf = ''.join([buf, recieve_socket.recv(int(x1*x2*x3 - block_size*count))])

#    print (len(buf), x1*x2*x3, count)
    
    arr = np.fromstring(buf, dtype=np.uint8).reshape((x1, x2, x3))
    bitmap = cv.CreateImageHeader((x2, x1), cv.IPL_DEPTH_8U, 3)
    cv.SetData(bitmap, arr.tostring(), arr.itemsize*x2*3)
    cv.ShowImage('recieved2', bitmap)
    if cv.WaitKey(1) & 0xFF == ord('q'):
      break

  recieve_socket.close()


cap = cv.CaptureFromCAM(1)

#t1 = threading.Thread(target=transmitter, args=(cap, ('127.0.0.1', 30090)))
t2 = threading.Thread(target=reciever)

#t1.start()
t2.start()

#t1.join()
t2.join()
