import cv
import numpy as np
import socket
import time
import errno


transmitter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  transmitter.connect(('127.0.0.1', 9091))
except socket.error, v:
	errorcode = v[0]
	if errorcode == errno.ECONNREFUSED:
		print "User you trying to connect to is not online"
		exit()
	print errorcode
	exit()

cap = cv.CaptureFromCAM(0)

while True:
  img = cv.QueryFrame(cap)
  cv.ShowImage('transmit', img)
  img = np.asarray(img[:,:])
  count = int(img.size/20480)
  start = time.time()
  transmitter.send(str(img.shape))
  transmitter.send(str(count))
  for i in range(count):
    transmitter.send(img.data[20480*i:(i+1)*20480])
  transmitter.send(img.data[20480*(count):])
  if cv.WaitKey(1) & 0xFF == ord('q'):
  	  break

transmitter.close()


