import cv2
import numpy
import socket
import sys

transmitter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

transmitter.connect(('127.0.0.1', 9091))

img = cv2.imread('test1.jpg')

print img.itemsize
print len(img)
print img.size
print str(img.shape)
print img.dtype


transmitter.send(str(img.shape))
transmitter.send(img.data[0:20480])
transmitter.close()
