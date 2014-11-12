import socket
import numpy as np
import time
import cv2


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('', 9091))
sock.listen(1)

reciever, addr = sock.accept()

#cv2.cv.NamedWindow("reciever", cv2.cv.CV_WINDOW_AUTOSIZE)

while True:
  start = time.time()
  shape = reciever.recv(13)
  count = int(reciever.recv(2))
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
  cv2.cv.ShowImage('reciever', bitmap)
 # cv2.imshow('recieved', ppp)
  if cv2.cv.WaitKey(10) & 0xFF == ord('q'):
    break

reciever.close()

