import numpy as np
import sys

arr = [1,2,3,4,5,6,7,8,9]



a = np.array(arr)
#print a

print len(a.data)

b = a.reshape((3,3))
print len(b.data)

#print b.tolist()
