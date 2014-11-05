import cv2 as cv
import numpy
import socket
import time
import sys

start = time.time()

cap = cv.VideoCapture(0)

transmitter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

transmitter.connect(('127.0.0.1', 9091))

while True:
  ret, img = cap.read()
  img_size = img.size
  count = int(img_size/20480)
  print str(img.shape), img.size
  transmitter.send(str(img.shape))
  transmitter.send(str(count))
  for i in range(count):
    #print i
    transmitter.send(img.data[20480*i:(i+1)*20480])
    print len(img.data[20480*(count):])
  transmitter.send(img.data[20480*(count):])


ransmitter.close()


end = time.time()
print end-start
