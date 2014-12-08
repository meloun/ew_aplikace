'''
Created on 18.9.2012

@author: Meloun
'''


mydict = {"keyA":{"key1":1,"key2":2}, "keyB":2, "keyC":3}
mydict2 = {"keyA":{"key1":1,"key2":2}, "keyB":2, "keyC":3}

def set_keys(d, keys, value):
    item = d
    for key in keys[:-1]:
        item = item[key]
    print "k",key[-1]
    item[keys[-1]] = value



print "mydict + mydict2", dict(mydict.items() + mydict2.items())
        
print mydict
set_keys(mydict, ["keyA", "key1"], 78)
print mydict