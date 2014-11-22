import sockets
import numpy as np
import cv
import threading

def transmitting(cameraCapture):
  transmit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  transmit_socket.connect(('127.0.0.1', 9091))


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


cap = cv.CaptureFromCAM(0)

