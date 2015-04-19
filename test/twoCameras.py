import cv
from time import sleep

cap0 = cv.CaptureFromCAM(0)
cap1 = cv.CaptureFromCAM(1)

print cap0, cap1

sleep(5)

while True:
  img = [cv.QueryFrame(cap0), cv.QueryFrame(cap1)]
  print img[0], img[1]
  sleep(10)
  cv.ShowImage('cap0', img[0])
  cv.ShowImage('cap1', img[1])
  if cv.WaitKey(10) &0xFF == ord('q'):
    break
