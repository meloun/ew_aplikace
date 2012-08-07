# -*- coding: utf-8 -*-
import collections

DATA = { u'spam': u'eggs', u'foo': frozenset([u'Gah!']), u'bar': { u'baz': 97 },
         u'list': [u'list', (True, u'Maybe'), set([u'and', u'a', u'set', 1])]}

def convert(data):    
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
    
def deconvert(data):    
    if isinstance(data, unicode):
        return data
    elif isinstance(data, str):
        return data.decode('utf-8')
    elif isinstance(data, collections.Mapping):        
        return dict(map(deconvert, data.iteritems()))
    elif isinstance(data, collections.Iterable):        
        return type(data)(map(deconvert, data))
    else:
        return data    

print DATA
print convert(DATA)
#print deconvert(convert(DATA))
print deconvert(DATA)

if(u'režnice' == "režnice"):
    print "ANO"