# -*- coding: utf-8 -*-
'''
Created on 09.10.2012

@author: z002ys1y
'''
from itertools import product


# map
#
#použije funkci pro každý prvek iterátoru
#vrací list s výsledky
def square(num):
    return num*num
print "map"
print map(str,('a',2,'c'))
print map(square,[1,2,3])



lists = [
    ['a', 'b'],
    [1, 2],
    ['i', 'ii'],
]
separator = '-'

# product
#
#pro dva iterovatelné výsledky, vrací jejich kombinace
#vrací iterátor s listy
print "product"
#for x in product(*[[1,2,3],[11,22,33],[111,222,333]]):
#    print x
print [x for x in product(*[[1,2,3],[11,22,33],[111,222,333]])]

