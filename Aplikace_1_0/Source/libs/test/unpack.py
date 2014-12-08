# -*- coding: utf-8 -*-
import struct
record = b'raymond   \x32\x12\x08\x01\x08'
name, serialnum, school, gradelevel = struct.unpack('<10sHHb', record)
mylist = struct.unpack('<10sHHb', record)

print "name:", name
print "serialnum:", serialnum
print "school:", school
print "gradelevel:", gradelevel


print "list:", mylist
print "list0:", mylist[0]
print "list1:", mylist[1]
print "list-length:", len(mylist)

