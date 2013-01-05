# -*- coding: utf-8 -*-
'''
Created on 16.7.2012

@author: Meloun
'''

import binascii
import sys


def codepage():
    s1 = u"Žluťoučký kůň pěl ďábelské ódy."
    s2 = "Žluťoučký kůň pěl ďábelské ódy."
    i1 = 0x12345678
    
    print "default encoding: ", sys.getdefaultencoding()
    print "stdout encoding:", sys.stdout.encoding
    
    print "\nUnicode string test"
    print "====================="
    print "test.. ", s1, type(s1)
    print "cp1250 test.. ",s1.encode('cp1250'), type(s1.encode('cp1250'))
    print "utf-8 test.. ",s1.encode('utf-8'), type(s1.encode('utf-8'))
    
    print "\nDefault string"
    print "====================="
    print "test.. ", s2, type(s2)
    print "cp1250 test.. ",s2.decode('utf-8').encode('cp1250'), type(s2.decode('utf-8').encode('cp1250'))
    print "utf-8 test.. ",s2.decode('utf-8'), type(s2.decode('utf-8'))
    
#    print "\nOperation"
#    print "====================="
#    a = type(unicode(s2))
#    print "unicode + default:", s1 + unicode(s2)
#    
#    print "\nInteger"
#    print "====================="
#    print i1, type(i1)
#    print str(i1), type(str(i1))
#    print hex(i1), type(hex(i1))
#    
#    print "\nOthers"
#    print "====================="
#    print "hex",s1.encode('hex'),type(s1.encode('hex'))
#    print "hexlify",binascii.hexlify(s1),type(binascii.hexlify(s1))
#    print "repr",repr(s1), type(repr(s1))
#    
#    mystring2 = '%0*x' % (8, 0x31323334) 
#    print mystring2.decode('hex')
#    print binascii.unhexlify(mystring2)

if __name__ == "__main__": 
    codepage()