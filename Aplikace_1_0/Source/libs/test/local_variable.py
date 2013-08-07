

mydict = {"a":1, "b":2, "c":3}
mylist = [1,2,3]

def myfunctionDict(mydict):
    mydict["a"] = 33
    return mydict

def myfunctionList(mylist):
    mylist[2] = 33
    return mylist

def myfunctionList2(mylist):
    aux_mylist = mylist[:]
    aux_mylist[2] = 33
    return aux_mylist



print mylist
print myfunctionList2(mylist)
print mylist


