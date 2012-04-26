# -*- coding: utf-8 -*-
from PyQt4 import Qt

'''cconvert integer(time in ms) to string (HH:MM:SS:mSmS)'''
def time_to_string(time):
    hours = time / (100*60*60)
    
    time = time % (100*60*60)
    minutes = time / (100*60)
    
    time = time % (100*60)
    seconds = time / (100)
    
    milliseconds = time % (100)
    
    return '%02d:%02d:%02d,%02d' %(hours, minutes, seconds, milliseconds)

def getUtf8String(item):
    
    #print "1",type(item)
    if type(item) is unicode:
        item = (item).encode('utf-8')
    #if type(item) is str:
    #    item = (item).encode('utf-8')
    if type(item) is Qt.QString:
        item = str(item.toUtf8())
    if type(item) is int:
        item=str(item)
    #print "2",type(item), item             
         
    return item

if __name__ == "__main__":
    import struct
    
    a = struct.pack('???', 1,1,1)
    print str(a)
    
    a = "žřš"
    b = u"žřš"
    c = 66
    d = Qt.QString(u"žřš")
    
    print a, type(a)
    print b, type(b)
    print c, type(c)
    print d, type(d)
    a = getUtf8String(a)
    b = getUtf8String(b)
    c = getUtf8String(c)
    d = getUtf8String(d)
    print a, type(a)
    print b, type(b)
    print c, type(c)
    print d, type(d)
    

print int(True)
print int(False)