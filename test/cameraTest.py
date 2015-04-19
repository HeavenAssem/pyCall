import cv

cap = cv.CaptureFromCAM(0)

while True:
  frame = cv.QueryFrame(cap)
  cv.ShowImage('cap 0', frame)
  cv.WaitKey(0)
