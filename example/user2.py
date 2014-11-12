import sys
import errno
import threading
import cv
import time
import socket
import numpy as np

block_size = 20480 #bytes

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
    print threading.current_thread().name, "started transmitting video"
    image = cv.QueryFrame(capture)
    if image != None:
      image = np.asarray(image[:,:])
      count = int(image.size/block_size)
      transmit_socket.send(str(image.shape))
      transmit_socket.send(str(count))
      for i in range(count):
        transmit_socket.send(image.data[block_size*i:block_size*(i+1)])
      transmit_socket.send(image.data[block_size*count:])
      if cv.WaitKey(1) & 0xFF == ord('q'):
        break
    
  transmit_socket.close()

def reciever():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.bind(('', 10091))
  sock.listen(1)
  
  print 'listening'
  recieve_socket, addr = sock.accept()
  print addr
  
  while True:
    shape = recieve_socket.recv(13)
    count = int(recieve_socket.recv(2))
    splitted = shape.split(',')
    x1 = int(splitted[0][1:])
    x2 = int(splitted[1][1:])
    x3 = int(splitted[2][:len(splitted[2])-1])
    
    buf = ''
    for i in range(count):
      buf = buf + reciever.recv(20480)
    buf = buf + reciever.recv(x1*x2*x3 - 20480*count)

    arr = np.fromstring(buf, dtype=np.uint8).reshape((x1, x2, x3))
    bitmap = cv2.cv.CreateImageHeader((x2, x1), cv2.cv.IPL_DEPTH_8U, 3)
    cv2.cv.SetData(bitmap, arr.tostring(), arr.itemsize*x2*3)
    cv2.cv.ShowImage('recieved', bitmap)
    if cv2.cv.WaitKey(10) & 0xFF == ord('q'):
      break

  recieve_socket.close()


print len(sys.argv)
print sys.argv


cap = cv.CaptureFromCAM(0)

t1 = threading.Thread(target=transmitter, args=(cap, ('127.0.0.1', 9090)))
t2 = threading.Thread(target=reciever)

t1.start()
t2.start()

t1.join()
t2.join()
