import cv2
import numpy
import socket
import time
import sys

start = time.time()

transmitter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

transmitter.connect(('127.0.0.1', 9091))

img = cv2.imread('test1.jpg')
img_size = img.size
count = int(img_size/20480)

print img.itemsize
print len(img)
print img_size, count
print str(img.shape)
print img.dtype


transmitter.send(str(img.shape))
transmitter.send(str(count))
for i in range(count):
  transmitter.send(img.data[20480*i:(i+1)*20480])
transmitter.send(img.data[20480*(count):])
transmitter.close()

end = time.time()
print end-start
