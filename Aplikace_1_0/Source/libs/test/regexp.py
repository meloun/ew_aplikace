'''
Created on 15.1.2013

@author: Meloun
'''
import re

#print re.sub(r'[^;]', '', 'abcd;e;yth;ac;ytwec')

mystring = "asd=22|23"

mydictstring = '{"cell":30, "time":30}'
myaa = {"cell":30, "time":30}


bb = [item.split("=") for item in mystring.split(";")]
print bb
print dict(bb)
#mydict =  dict(item.split("=") for item in mystring.split(";"))
#print mydict

#print mydictstring

#import json
#mydict = json.loads(mydictstring)
#print mydict



