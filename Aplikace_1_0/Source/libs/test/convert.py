# -*- coding: utf-8 -*-
import collections

DATA = { u'spam': u'eggs', u'foo': frozenset([u'Gah!']), u'bar': { u'baz': 97 },
         u'list': [u'list', (True, u'Maybe'), set([u'and', u'a', u'set', 1])]}

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
    return data    

print DATA, type(DATA)
print toString(DATA), type(toString(DATA))
#print deconvert(convert(DATA))
print toUnicode(DATA), type(toUnicode(DATA))

if(u'režnice' == "režnice"):
    print "ANO"