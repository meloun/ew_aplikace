'''
Created on 27.9.2012

@author: Meloun
'''
from threading import Timer

def delayed(seconds, f):        
    t = Timer(seconds, f)
    t.start()


def foo():

    print('foo')

#delayed(1, foo)

t = Timer(1, foo)
t.start()
print('dudee')