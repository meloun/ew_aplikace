# -*- coding: utf-8 -*-
from PyQt4 import Qt
import unicodedata
import collections

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
        item = item.encode('utf-8')        
    #if type(item) is str:
    #    item = (item).encode('utf-8')
    if type(item) is Qt.QString:        
        item = str(item.toUtf8())
    if type(item) is int:        
        item=str(item)
    #print "2",type(item), item             
         
    return item

def toString(data):    
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(toString, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(toString, data))    
    return data
    
def toUnicode(data, decode = 'utf-8', decode_number = True):    
    if isinstance(data, unicode):
        return data
    elif isinstance( data, ( int, long ) ) and decode_number:
        return unicode(data)
    elif isinstance(data, str):
        return unicode(data, decode)
    elif isinstance(data, collections.Mapping):        
        return dict(map(toUnicode, data.iteritems()))
    elif isinstance(data, collections.Iterable):        
        return type(data)(map(toUnicode, data))    
    return unicode(data)

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def get_filename(input_str):
    filename = remove_accents(input_str)    
    filename = filename.replace(' ', '_')        
    return filename
if __name__ == "__main__":
    import struct
    
    DATA = { u'spam': u'eggs', u'foo': frozenset([u'Gah!']), u'bar': { u'baz': 97 },
         u'list': [u'list', (True, u'Maybe'), set([u'and', u'a', u'set', 1])]}
    
    print DATA, type(DATA)
    print toString(DATA), type(toString(DATA))
    print toUnicode(DATA), type(toUnicode(DATA))

    
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
