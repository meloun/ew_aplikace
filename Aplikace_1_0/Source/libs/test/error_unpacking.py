# -*- coding: utf-8 -*-
import struct
record = b'\x01\x02\x03\x04\x05'


values = struct.unpack('<bbbbb', record)
keys = ['key{0}'.format(x) for x in range(1, len(values)+1)]
mydict = dict(zip(keys, values))

print "mydict", mydict




