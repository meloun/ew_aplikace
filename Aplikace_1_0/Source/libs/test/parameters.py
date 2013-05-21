'''
Created on 04.01.2013

@author: z002ys1y
'''
mydict = {"key1":"value1", "key2":"value2"}

def myfunction(item):
    print "f1",item
    item = "changed"
    print "f2",item
        
def myfunction2(dictpar):
    print "f1",dictpar    
    dictpar["key1"] = "changed"
    print "f2",dictpar    


print mydict
myfunction(mydict["key1"])
print mydict
print "-----"
print mydict
myfunction2(mydict)
print mydict
    
    