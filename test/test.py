import struct

dct = {}
for i in range(1000000):
  dct[len(struct.pack('i', i))] = 0

print dct.keys()
