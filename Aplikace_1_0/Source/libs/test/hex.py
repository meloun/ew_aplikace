'''
Created on 11.11.2013

@author: Meloun
'''
s = "abcd"

print "{:}".format((12,13))
s2 = s.encode('hex')
print s2, type(s2)
for c in s:
    print c
    print c.encode('hex')

print (",".join(c.encode('hex') for c in s))
print ":".join(c.encode('hex') for c in s)